/**
 * AI Text Summarizer - Main JavaScript
 * Handles UI interactions and form functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Show loader when form is submitted
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            const submitBtn = document.getElementById('submit-btn');
            const loader = document.getElementById('loader');
            if (submitBtn && loader) {
                loader.classList.remove('hidden');
                submitBtn.disabled = true;
            }
        });
    }
    // Show file name when selected
    const fileInput = document.getElementById('file-input');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileName = this.files[0]?.name || '';
            document.getElementById('file-name').textContent = fileName ? `Selected: ${fileName}` : '';
        });
    }
    
    // Toggle options based on method selection
    const methodSelect = document.getElementById('method');
    if (methodSelect) {
        methodSelect.addEventListener('change', function() {
            const isExtractive = this.value === 'extractive';
            document.querySelector('.extractive-options').classList.toggle('hidden', !isExtractive);
            document.querySelector('.abstractive-options').classList.toggle('hidden', isExtractive);
        });
    }
    
    // Update ratio value display
    const ratioInput = document.getElementById('ratio');
    if (ratioInput) {
        // Update display when input changes
        ratioInput.addEventListener('input', function() {
            document.getElementById('ratio-value').textContent = Math.round(this.value * 100) + '%';
        });
        
        // Initialize display with current value when page loads
        document.getElementById('ratio-value').textContent = Math.round(ratioInput.value * 100) + '%';
    }
    
    // Validate min/max length relationship
    const minLengthInput = document.getElementById('min-length');
    const maxLengthInput = document.getElementById('max-length');
    const MIN_BUFFER = 10; // Minimum difference between min and max length
    
    if (minLengthInput && maxLengthInput) {
        // When min length changes
        minLengthInput.addEventListener('change', function() {
            const minVal = parseInt(this.value);
            const maxVal = parseInt(maxLengthInput.value);
            
            // If min length is greater than or equal to max length,
            // increase max length to accommodate the new min length
            if (minVal >= maxVal) {
                maxLengthInput.value = minVal + MIN_BUFFER;
            }
        });
        
        // When max length changes
        maxLengthInput.addEventListener('change', function() {
            const maxVal = parseInt(this.value);
            const minVal = parseInt(minLengthInput.value);
            
            // If max length is less than or equal to min length,
            // decrease min length to accommodate the new max length
            if (maxVal <= minVal) {
                minLengthInput.value = Math.max(10, maxVal - MIN_BUFFER);
            }
        });
    }
    
    // Copy summary to clipboard
    const copyBtn = document.getElementById('copy-btn');
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            const summaryText = document.querySelector('.summary-text p').textContent;
            navigator.clipboard.writeText(summaryText)
                .then(() => {
                    this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    setTimeout(() => {
                        this.innerHTML = '<i class="fas fa-copy"></i> Copy';
                    }, 2000);
                })
                .catch(err => {
                    console.error('Failed to copy text: ', err);
                });
        });
    }
    
    // Download summary as text file
    const downloadBtn = document.getElementById('download-btn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            const summaryText = document.querySelector('.summary-text p').textContent;
            const blob = new Blob([summaryText], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'summary.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }
});
