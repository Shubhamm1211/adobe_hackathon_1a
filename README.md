# Adobe Hackathon 2025 - Round 1A: Document Outline Extractor

This project is a solution for Round 1A of the Adobe "Connecting the Dots" Hackathon. It's a Python application, packaged in Docker, that extracts a structured outline (Title, H1, H2, H3) from PDF documents.

## Approach

[cite_start]The solution uses a rule-based (heuristic) approach to analyze the structure of a PDF without relying on large machine learning models, ensuring it meets the strict performance and size constraints (<200MB model size, <10s execution)[cite: 695, 696].

The core logic involves:
1.  **Base Font Identification**: The script first identifies the most common font size in the document, which is assumed to be the main body text.
2.  **Numbered Heading Detection**: It uses regular expressions (regex) to find numbered headings (e.g., `1.1`, `Appendix A`), as this is a highly reliable indicator of structure.
3.  **Dynamic Style Analysis**: For non-numbered headings, the script dynamically identifies the font sizes used for headings (larger than the base size and bold). It ranks these sizes to determine the H1, H2, and H3 levels for that specific document.
4.  **Title Extraction**: The title is identified by searching for prominent, large-font text near the top of the first page.

This hybrid approach is robust, fast, and adapts to different document layouts.

## Models or Libraries Used

* **`PyMuPDF` (`fitz`)**: A high-performance Python library for PDF parsing. It's used to extract text blocks along with their metadata (font size, font name, position).
* No external machine learning models are used.

## How to Build and Run the Solution

The solution is containerized using Docker.

**1. Build the Docker image:**
The evaluation will use a command similar to this:
```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .