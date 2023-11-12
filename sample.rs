#!/bin/sh
exec docker run  --rm -it  -v "`pwd`:/sync" frantzme/rustdev:lite /bin/single_run ./$0
//add :mac or :win to the end of the file name compile for those architectures
//also, any comment starting with //* goes directly in the cargo.toml under dependencies
//* clap = { version = "4.1.6", features = ["derive"]}
//* fstrings = "0.2.3"
//https://www.tutorialspoint.com/rust/rust_data_types.htm
use std::process::Command;
use clap::Parser;

#[macro_use]
extern crate fstrings;

/// Simple program to greet a person
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
   /// Name of the person to greet
   #[arg(short, long, default_value_os = "sample")]
   name: String,

   /// Number of times to greet
   #[arg(short, long, default_value_t = 1)]
   count: u8,
}

fn main() {
   let args = Args::parse();

   for _ in 0..args.count {
       //println!("Hello {}!", args.name);
       println_f!("Hello {args.name}");
   }

   let output = Command::new("ls").output().expect("Failed to execute the process");
   //println!("stdout: {}", String::from_utf8_lossy(&output.stdout));
   let lines = String::from_utf8_lossy(&output.stdout).to_string();
   //println!("lines :> {}",lines);
    for line in lines.split('\n') {
        if !line.is_empty()
        {
            //println!("!> {}",line);
            println_f!("!> {line}");
        }
    }

}

//READ FROM FILE EXAMPLE
//https://levelup.gitconnected.com/working-with-csv-data-in-rust-7258163252f8
// Reads data from a file into a reader and deserializes each record
//
// # Error
//
// If an error occurs, the error is returned to `main`.
//fn read_from_file(path: &str) -> Result<(), Box<dyn Error>> {
//    // Creates a new csv `Reader` from a file
//    let mut reader = csv::Reader::from_path(path)?;
//
//    // Retrieve and print header record
//    let headers = reader.headers()?;
//    println!("{:?}", headers);
//
//    // `.deserialize` returns an iterator of the internal
//    // record structure deserialized
//    for result in reader.deserialize() {
//        let record: Customer = result?;
//
//        println!("{:?}", record);
//    }
//
//    Ok(())
//}

//READ FILE LINE BY LINE
//https://doc.rust-lang.org/rust-by-example/std_misc/file/read_lines.html
//use std::fs::File;
//use std::io::{ self, BufRead, BufReader };
//
//fn read_lines(filename: String) -> io::Lines<BufReader<File>> {
//    // Open the file in read-only mode.
//    let file = File::open(filename).unwrap(); 
//    // Read the file line by line, and return an iterator of the lines of the file.
//    return io::BufReader::new(file).lines(); 
//}

//LUA USAGE
//https://docs.rs/hlua/latest/hlua/
//https://www.lua.org/pil/16.html CREATE AN OBJECT
//https://gist.github.com/obikag/6118422 TO CSV

//SQLITE USAGE
//https://docs.rs/sqlite/latest/sqlite/
//https://rust-lang-nursery.github.io/rust-cookbook/database/sqlite.html

//DataFrame Usage
//https://docs.rs/polars/latest/polars/

//Option Usage
//https://doc.rust-lang.org/std/option/enum.Option.html