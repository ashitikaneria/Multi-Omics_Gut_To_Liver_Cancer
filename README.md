# Multi-Omics Analysis: Gut Microbiome to Liver Cancer Progression

## 🔬 Project Overview

This repository contains a comprehensive multi-omics analysis investigating the relationship between **gut microbiome composition** and **advanced liver disease progression**. The project integrates **metagenomic functional profiling** and **transcriptomic data** to identify microbial taxa and genes associated with liver cancer development.

**Key Research Focus:**
- Comparative analysis of healthy controls vs. advanced liver disease samples
- Functional and taxonomic abundance profiling
- Gene expression analysis with statistical significance testing
- Integration of KEGG pathway annotations and metabolic gene clusters (KO)

---

## 📊 Data Overview

### Sample Composition
- **Total Samples:** 92 samples
- **Healthy Controls:** 44 samples
- **Advanced Liver Disease:** 48 samples
- **Data Source:** BioProject PRJNA872871 (SRA)

### Data Files

| File | Description |
|------|-------------|
| `InputMetadata.txt` | Sample metadata mapping (Sample ID → Disease Status) |
| `DESeq2_All gene name.xlsx` | Complete RNA-seq differential expression analysis |
| `significant gene .xlsx` | Filtered significant genes (p-adj < 0.05) |
| `KO_full_annotation.xlsx` | KEGG Ortholog (KO) annotations with functional pathways |
| `func.KO.abd.xlsx` | KO functional abundance matrix across samples |
| `kegg_abundance_comparison.xlsx` | KEGG pathway abundance comparison analysis |
| `taxa.phylum.Abd.distribution.pdf` | Phylum-level taxonomic abundance distribution plots |
| `taxa.genus.Abd.distribution.pdf` | Genus-level taxonomic abundance distribution plots |
| `func.l2.Abd.distribution.pdf` | Functional (L2) level abundance distribution |
| `func.l3.Abd.distribution.pdf` | Functional (L3) level abundance distribution |
| `fastp_summary.xlsx` | Quality control metrics from read trimming |
| `seqs.list` | Sequence accession list for analysis |

---

## 🛠️ Pipeline Components

### 1. **Data Acquisition** (`SRA_fetch.py`)
- Automated retrieval of raw sequencing data from NCBI SRA
- Filters samples by disease status (Healthy Control & Advanced Liver Disease)
- Generates download scripts with SRA Toolkit integration
- Creates metadata summaries for quality tracking

**Usage:**
```bash
pip install requests pandas
python SRA_fetch.py
bash download_fastq.sh /path/to/output
```

### 2. **Quality Control** (`run_fastp.sh`)
- Read trimming and quality filtering using fastp
- Adapter removal and polyN filtering
- Performance metrics captured in `fastp_summary.xlsx`

### 3. **Sample Filtering** (`filt_samples.py`)
- Removes low-quality samples below quality thresholds
- Validates sample integrity across metadata

### 4. **Taxonomic & Functional Profiling**
- **Taxonomic:** Phylum and Genus-level abundance analysis
- **Functional:** KEGG Ortholog (KO) and metabolic pathway profiling
- Distribution analysis across disease groups

### 5. **Differential Analysis** (`higher_abd.py`)
- Identifies taxa/genes with significantly higher abundance in disease group
- Statistical testing and abundance comparison
- Generates comparison matrices

### 6. **Annotation & Integration** (`parse_information.py`, `all annotation .py`)
- KEGG pathway annotation parsing
- Gene functional classification
- Metabolic pathway mapping

---

## 📈 Key Analysis Outputs

### Differentially Abundant Features
- **Significant Genes:** Genes with adjusted p-value < 0.05
- **Higher Abundance in Disease:** Microbial functions enriched in advanced liver disease
- **Statistical Method:** DESeq2 for RNA-seq; abundance comparison for metagenomic data

### Pathway Analysis
- KEGG pathway enrichment in disease vs. healthy samples
- Functional annotation at multiple hierarchical levels (L2, L3)
- Abundance distributions visualized for comparison

### Taxonomic Insights
- Phylum-level community structure
- Genus-level differential abundance
- Distribution plots for exploratory data analysis

---

## 🔧 Technical Requirements

### Dependencies
```
Python 3.7+
pandas
requests
DESeq2 (R/Python)
NCBI SRA Toolkit
fastp
```

### Installation
```bash
# Clone repository
git clone https://github.com/ashitikaneria/Multi-Omics_Gut_To_Liver_Cancer.git
cd Multi-Omics_Gut_To_Liver_Cancer

# Install Python dependencies
pip install pandas requests

# Install bioinformatics tools (conda recommended)
conda install -c bioconda sra-tools fastp
```

---

## 📑 Workflow Steps

1. **Fetch SRA Data**
   ```bash
   python SRA_fetch.py  # Downloads metadata, generates download scripts
   bash download_fastq.sh /output/path  # Downloads FASTQ files
   ```

2. **Quality Control**
   ```bash
   bash run_fastp.sh  # Trims and filters reads
   ```

3. **Sample Filtering**
   ```bash
   python filt_samples.py  # Removes low-quality samples
   ```

4. **Metagenomic & RNA-seq Analysis**
   - Taxonomic profiling (external tool output)
   - Functional profiling via KEGG KO
   - Gene expression analysis via DESeq2

5. **Integration & Visualization**
   ```bash
   python parse_information.py  # Parse annotations
   python higher_abd.py  # Identify higher abundance features
   python all\ annotation\ .py  # Comprehensive annotation
   ```

---

## 📊 File Structure

```
Multi-Omics_Gut_To_Liver_Cancer/
├── README.md                              # Project documentation
├── InputMetadata.txt                      # Sample classification
├── SRA_fetch.py                           # Data download script
├── run_fastp.sh                           # QC pipeline
├── filt_samples.py                        # Sample filtering
├── parse_information.py                   # Info parsing
├── higher_abd.py                          # Abundance analysis
├── all annotation .py                     # Annotation integration
│
├── Data Files (Excel/TSV):
├── DESeq2_All gene name.xlsx              # Gene expression matrix
├── significant gene .xlsx                 # Filtered DE genes
├── KO_full_annotation.xlsx                # KEGG annotations
├── func.KO.abd.xlsx                       # KO abundance matrix
├── kegg_abundance_comparison.xlsx         # Pathway comparison
├── fastp_summary.xlsx                     # QC metrics
│
├── Visualizations (PDF):
├── taxa.phylum.Abd.distribution.pdf       # Phylum plots
├── taxa.genus.Abd.distribution.pdf        # Genus plots
├── func.l2.Abd.distribution.pdf           # Functional L2 plots
├── func.l3.Abd.distribution.pdf           # Functional L3 plots
│
└── seqs.list                              # SRA accessions
```

---

## 🎯 Research Questions Addressed

1. **How do microbial communities differ between healthy and advanced liver disease patients?**
   - Addressed through taxonomic profiling at phylum and genus levels

2. **What microbial functions are enriched in disease progression?**
   - Analyzed via KEGG pathway and KO functional abundance

3. **Which genes show significant differential expression?**
   - Identified through DESeq2 analysis with multiple testing correction

4. **How do metabolic pathways associate with disease status?**
   - Pathway-level analysis with abundance comparison across groups

---

## 📖 Usage Examples

### Viewing Differential Genes
Open `significant gene .xlsx` to see filtered DE genes with:
- Log2 fold changes
- Adjusted p-values
- Mean expression levels

### Exploring KEGG Pathways
Check `kegg_abundance_comparison.xlsx` for:
- Pathway functional annotations
- Abundance differences between groups
- Enrichment patterns

### QC Assessment
Review `fastp_summary.xlsx` for:
- Read count statistics
- Quality score distributions
- Trimming efficiency

---

## 👤 Author

**Ashit Kaneria**  
[GitHub Profile](https://github.com/ashitikaneria)

---

## 📝 License

This project is provided as-is for research purposes. 

---

## 🔗 References

- **BioProject:** PRJNA872871
- **Data Source:** NCBI SRA (Sequence Read Archive)
- **Methods:** DESeq2, KEGG Functional Annotation, Metagenomic Profiling

---

## ⚠️ Important Notes

- Ensure NCBI email address is updated in `SRA_fetch.py` before running
- SRA downloads may require significant storage (depends on sample count)
- Quality thresholds in `filt_samples.py` should be adjusted based on your analysis goals
- All analysis assumes properly formatted input metadata

---

## 🤝 Contributing

For improvements, bug fixes, or suggestions, please open an issue or contact the author.

---

## 📞 Support

For issues related to:
- **NCBI SRA downloads:** Check NCBI SRA website and ensure Entrez tools are properly installed
- **Bioinformatics tools:** Refer to tool-specific documentation (fastp, SRA Toolkit)
- **Statistical analysis:** Verify input file formats and metadata structure

---

**Last Updated:** June 2026  
**Project Status:** Active Research
