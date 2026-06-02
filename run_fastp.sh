#!/bin/bash

echo "Starting fastp processing..."

#Loop through all forward reads
for file in *_1.fastq.gz
do
    #Extract sample name
    base=$(basename "$file" _1.fastq.gz)

    #Check if reverse file exists
    if [[ -f "${base}_2.fastq.gz" ]]; then
        
        echo "Processing sample: $base"

        #Create folder for this sample
        mkdir -p fastp_output/${base}

        fastp \
        -i ${base}_1.fastq.gz \
        -I ${base}_2.fastq.gz \
        -o fastp_output/${base}/filt_${base}_1.fastq \
        -O fastp_output/${base}/filt_${base}_2.fastq \
        -t 15 -T 15 -q 20 --length_required 280 \
        --average_qual 20 \
        -j fastp_output/${base}/${base}.json \
        -h fastp_output/${base}/${base}.html \
        -R "${base} fastp report" \
        -w 10

        echo "Completed: $base"

    else
        echo "Missing pair for $base"
    fi
done

echo "All samples processed successfully!"
