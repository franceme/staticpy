#!/usr/bin/env python3

import os,sys

def write(file, content,delete=False):
	with open(file, "w+") as writer:
		writer.write(content)

write("Makefile","""#links
#* https://github.com/quadratichq/quadratic/issues/416
name=quadratic
default:: full

download:
	#The one right before license change
	#wget https://github.com/quadratichq/quadratic/archive/d6e9b05952d26eb7130cd308e8fa0cb805c7734e.zip
	#The latest
	#wget https://github.com/quadratichq/quadratic/archive/refs/heads/main.zip
	#The one from whoever added the docker file
	wget https://github.com/irjensen/quadratic/archive/30e11ae44625059b722150d70559491596c92b6c.zip
	7z x *.zip 
	rm *.zip
	mv $(name)-* $(name)
	cp Dockerfile $(name)/
build:
	if test -d $(name)/;then echo exists;else make download;fi
	cd $(name)/ && docker build -t $(name) --platform=linux/amd64 .
run:
	cd $(name)/ && docker run --platform linux/amd64 -p 3000:3000 $(name)

full:build run
""")

write("Dockerfile","""FROM rust:latest

# Install npm
RUN apt-get update && apt-get install -y npm

# Install wasm-pack
RUN curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh

# Add wasm32 target
RUN rustup target add wasm32-unknown-unknown

# Copy package.json and package-lock.json
COPY package*.json ./

# Copy the rest of the files
COPY . .

# Build Rust/WASM
RUN npm run build:wasm

# Install dependencies
RUN npm install


# Start the app
CMD ["npm", "start"]
""")