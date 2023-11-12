#!/bin/bash

cd /tmp/ \
&& apt-get install --upgrade curl zstd \
&& curl -sL https://dist.ballerina.io/downloads/2201.7.1/ballerina-2201.7.1-swan-lake-linux-x64.deb --output ballerina.deb \
&& ar x ballerina.deb \
&& zstd -d < control.tar.zst | xz > control.tar.xz \
&& zstd -d < data.tar.zst | xz > data.tar.xz \
&& ar -m -c -a sdsd /tmp/ballerina.deb debian-binary control.tar.xz data.tar.xz \
&& rm debian-binary control.tar.xz data.tar.xz control.tar.zst data.tar.zst ballerina.deb \
&& dpkg -i ballerina.deb