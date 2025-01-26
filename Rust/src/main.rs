// src/main.rs
use anyhow::{Context, Result};
use clap::{Parser, ValueEnum};
use lopdf::Document;
use reqwest::blocking::Client;
use std::{
    fs::{self, File},
    io::{self, copy, Write},
    path::{Path, PathBuf},
};
use urlencoding::encode;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    /// Directorio con archivos PDF (default: ../PDFs/)
    #[arg(short, long, default_value = "../PDFs/")]
    pdf_dir: PathBuf,

    /// Directorio de salida para audios (default: ../AUDIOS/)
    #[arg(short, long, default_value = "../AUDIOS/")]
    output_dir: PathBuf,

    /// Idioma para síntesis de voz
    #[arg(short, long, default_value = "es")]
    lang: Language,
}

#[derive(Debug, Clone, ValueEnum)]
enum Language {
    Es,
    En,
}

impl std::fmt::Display for Language {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Language::Es => write!(f, "es"),
            Language::En => write!(f, "en"),
        }
    }
}

fn main() -> Result<()> {
    let args = Args::parse();
    
    fs::create_dir_all(&args.pdf_dir)
        .with_context(|| format!("No se pudo crear directorio PDF: {}", args.pdf_dir.display()))?;
    
    fs::create_dir_all(&args.output_dir)
        .with_context(|| format!("No se pudo crear directorio de salida: {}", args.output_dir.display()))?;

    let pdf_files = get_pdf_list(&args.pdf_dir)?;
    let selected_pdf = show_interactive_menu(&pdf_files)?;
    
    let output_path = args.output_dir.join(
        selected_pdf.file_stem()
            .unwrap_or_default()
            .to_str()
            .unwrap_or("output")
            .to_owned() + ".mp3"
    );
    
    process_pdf(&selected_pdf, &output_path, &args.lang.to_string())?;
    
    println!("\n✅ Conversión completada: {}", output_path.display());
    Ok(())
}

fn get_pdf_list(pdf_dir: &Path) -> Result<Vec<PathBuf>> {
    let mut pdf_files = Vec::new();
    
    for entry in fs::read_dir(pdf_dir)
        .with_context(|| format!("No se pudo leer directorio: {}", pdf_dir.display()))? 
    {
        let path = entry?.path();
        if path.is_file() && path.extension().map_or(false, |ext| ext == "pdf") {
            pdf_files.push(path);
        }
    }
    
    if pdf_files.is_empty() {
        Err(anyhow::anyhow!("No se encontraron archivos PDF en {}", pdf_dir.display()))
    } else {
        Ok(pdf_files)
    }
}

fn show_interactive_menu(pdf_files: &[PathBuf]) -> Result<PathBuf> {
    println!("\n📚 Archivos PDF disponibles:");
    for (i, path) in pdf_files.iter().enumerate() {
        println!("  {}) {}", i + 1, path.file_name().unwrap_or_default().to_str().unwrap_or(""));
    }
    
    loop {
        print!("\nSeleccione un archivo (1-{}): ", pdf_files.len());
        io::stdout().flush()?;
        
        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        
        match input.trim().parse::<usize>() {
            Ok(n) if n >= 1 && n <= pdf_files.len() => 
                return Ok(pdf_files[n - 1].clone()),
            _ => println!("Selección inválida. Intente nuevamente."),
        }
    }
}

fn process_pdf(pdf_path: &Path, output_path: &Path, lang: &str) -> Result<()> {
    let text = extract_pdf_text(pdf_path)
        .with_context(|| format!("Error procesando PDF: {}", pdf_path.display()))?;
    
    let chunks = split_text(&text, 200);
    
    if chunks.is_empty() {
        return Err(anyhow::anyhow!("El PDF no contiene texto extraíble"));
    }
    
    generate_speech(&chunks, output_path, lang)
        .with_context(|| format!("Error generando audio: {}", output_path.display()))?;
    
    Ok(())
}

fn extract_pdf_text(pdf_path: &Path) -> Result<String> {
    let doc = Document::load(pdf_path)
        .with_context(|| format!("Error cargando PDF: {}", pdf_path.display()))?;
    
    let mut text = String::new();
    
    for (page_num, page_id) in doc.get_pages().iter().enumerate() {
        let page_text = doc.extract_text(&[*page_id.0]) // Corregido aquí: *page_id.0
            .with_context(|| format!("Error extrayendo texto de página {}", page_num + 1))?;
        
        text.push_str(&clean_text(&page_text));
        text.push('\n');
    }
    
    Ok(text)
}

fn clean_text(text: &str) -> String {
    text.replace("-\n", "")
        .replace('\u{ad}', "")
        .lines()
        .map(|line| line.trim())
        .filter(|line| !line.is_empty())
        .collect::<Vec<_>>()
        .join(" ")
}

fn split_text(text: &str, chunk_size: usize) -> Vec<String> {
    text.chars()
        .collect::<Vec<_>>()
        .chunks(chunk_size)
        .map(|chunk| chunk.iter().collect::<String>())
        .collect()
}

fn generate_speech(chunks: &[String], output_path: &Path, lang: &str) -> Result<()> {
    let client = Client::new();
    let mut output_file = File::create(output_path)
        .with_context(|| format!("Error creando archivo: {}", output_path.display()))?;
    
    println!("\n🔊 Procesando {} fragmentos de texto...", chunks.len());
    
    for (i, chunk) in chunks.iter().enumerate() {
        print!("  Fragmento {}/{}... ", i + 1, chunks.len());
        io::stdout().flush()?;
        
        let encoded_text = encode(chunk);
        let url = format!(
            "https://translate.google.com/translate_tts?ie=UTF-8&q={}&tl={}&client=tw-ob",
            encoded_text, lang
        );
        
        let response = client
            .get(&url)
            .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            .send()
            .with_context(|| format!("Error en solicitud HTTP para fragmento {}", i + 1))?;
        
        if !response.status().is_success() {
            return Err(anyhow::anyhow!(
                "Error en API TTS (Código {}): {}",
                response.status(),
                response.text()?
            ));
        }
        
        let content = response.bytes() // Corregido aquí: removido 'mut'
            .with_context(|| format!("Error leyendo respuesta para fragmento {}", i + 1))?;
        
        copy(&mut content.as_ref(), &mut output_file)
            .with_context(|| format!("Error escribiendo fragmento {} en archivo", i + 1))?;
        
        println!("✅");
    }
    
    Ok(())
}