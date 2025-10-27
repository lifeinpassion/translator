// Universal Translator - Frontend JavaScript

// Tab Management
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all tabs
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

        // Add active class to clicked tab
        btn.classList.add('active');
        const tabId = btn.getAttribute('data-tab') + '-tab';
        document.getElementById(tabId).classList.add('active');
    });
});

// Text Translation
const sourceText = document.getElementById('source-text');
const targetText = document.getElementById('target-text');
const sourceLang = document.getElementById('source-lang');
const targetLang = document.getElementById('target-lang');
const translateBtn = document.getElementById('translate-btn');
const charCount = document.getElementById('char-count');
const detectedLang = document.getElementById('detected-lang');
const translationInfo = document.getElementById('translation-info');

// Character counter
sourceText.addEventListener('input', () => {
    const count = sourceText.value.length;
    charCount.textContent = `${count} / 5000`;

    if (count > 5000) {
        charCount.style.color = 'var(--error-color)';
    } else {
        charCount.style.color = 'var(--text-light)';
    }
});

// Translate text
translateBtn.addEventListener('click', async () => {
    const text = sourceText.value.trim();

    if (!text) {
        alert('Please enter text to translate');
        return;
    }

    translateBtn.disabled = true;
    translateBtn.textContent = 'Translating...';
    translationInfo.textContent = '';

    try {
        const response = await fetch('/api/translate-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                source_lang: sourceLang.value,
                target_lang: targetLang.value
            })
        });

        const data = await response.json();

        if (response.ok) {
            targetText.textContent = data.translated_text;
            translationInfo.textContent = `Translated using ${data.tier_used} tier`;

            // Show detected language if auto-detect was used
            if (sourceLang.value === 'auto') {
                detectedLang.textContent = `Detected: ${data.source_lang}`;
            }
        } else {
            alert('Translation error: ' + data.error);
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    } finally {
        translateBtn.disabled = false;
        translateBtn.textContent = 'Translate';
    }
});

// Auto-translate on Enter key
sourceText.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        translateBtn.click();
    }
});

// Clear button
document.getElementById('clear-source').addEventListener('click', () => {
    sourceText.value = '';
    targetText.textContent = '';
    charCount.textContent = '0 / 5000';
    detectedLang.textContent = '';
    translationInfo.textContent = '';
});

// Copy button
document.getElementById('copy-translation').addEventListener('click', () => {
    const text = targetText.textContent;
    if (text) {
        navigator.clipboard.writeText(text).then(() => {
            const btn = document.getElementById('copy-translation');
            const originalText = btn.textContent;
            btn.textContent = 'Copied!';
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        });
    }
});

// Swap languages
document.getElementById('swap-langs').addEventListener('click', () => {
    const temp = sourceLang.value;
    sourceLang.value = targetLang.value;
    targetLang.value = temp;

    // Also swap text
    const tempText = sourceText.value;
    sourceText.value = targetText.textContent;
    targetText.textContent = tempText;
});

// Document Translation
const docUploadArea = document.getElementById('doc-upload-area');
const docFileInput = document.getElementById('doc-file-input');
const docFileInfo = document.getElementById('doc-file-info');
const docFileName = document.getElementById('doc-file-name');
const docFileSize = document.getElementById('doc-file-size');
const translateDocBtn = document.getElementById('translate-doc-btn');
const docProgress = document.getElementById('doc-progress');
const docProgressFill = document.getElementById('doc-progress-fill');
const docProgressText = document.getElementById('doc-progress-text');
const docResult = document.getElementById('doc-result');
const downloadDocBtn = document.getElementById('download-doc-btn');

let currentDocFile = null;
let downloadDocUrl = null;

docUploadArea.addEventListener('click', () => {
    docFileInput.click();
});

docUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    docUploadArea.style.borderColor = 'var(--secondary-color)';
});

docUploadArea.addEventListener('dragleave', () => {
    docUploadArea.style.borderColor = 'var(--border-color)';
});

docUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    docUploadArea.style.borderColor = 'var(--border-color)';

    const file = e.dataTransfer.files[0];
    if (file) {
        handleDocFile(file);
    }
});

docFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleDocFile(file);
    }
});

function handleDocFile(file) {
    currentDocFile = file;

    // Display file info
    docFileName.textContent = file.name;
    docFileSize.textContent = formatFileSize(file.size);

    docUploadArea.style.display = 'none';
    docFileInfo.style.display = 'block';
    docResult.style.display = 'none';
}

translateDocBtn.addEventListener('click', async () => {
    if (!currentDocFile) return;

    const formData = new FormData();
    formData.append('file', currentDocFile);
    formData.append('source_lang', document.getElementById('doc-source-lang').value);
    formData.append('target_lang', document.getElementById('doc-target-lang').value);

    translateDocBtn.disabled = true;
    docFileInfo.style.display = 'none';
    docProgress.style.display = 'block';

    // Simulate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 5;
        if (progress >= 90) {
            clearInterval(progressInterval);
        }
        docProgressFill.style.width = progress + '%';
    }, 500);

    try {
        const response = await fetch('/api/translate-document', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        clearInterval(progressInterval);
        docProgressFill.style.width = '100%';

        if (response.ok) {
            downloadDocUrl = data.download_url;
            docProgress.style.display = 'none';
            docResult.style.display = 'block';
        } else {
            alert('Translation error: ' + data.error);
            docFileInfo.style.display = 'block';
            docProgress.style.display = 'none';
        }
    } catch (error) {
        clearInterval(progressInterval);
        alert('Network error: ' + error.message);
        docFileInfo.style.display = 'block';
        docProgress.style.display = 'none';
    } finally {
        translateDocBtn.disabled = false;
    }
});

downloadDocBtn.addEventListener('click', () => {
    if (downloadDocUrl) {
        window.location.href = downloadDocUrl;
    }
});

// Image Translation
const imgUploadArea = document.getElementById('img-upload-area');
const imgFileInput = document.getElementById('img-file-input');
const imgFileInfo = document.getElementById('img-file-info');
const imgPreview = document.getElementById('img-preview');
const translateImgBtn = document.getElementById('translate-img-btn');
const imgProgress = document.getElementById('img-progress');
const imgProgressFill = document.getElementById('img-progress-fill');
const imgProgressText = document.getElementById('img-progress-text');
const imgResult = document.getElementById('img-result');
const imgOriginal = document.getElementById('img-original');
const imgTranslated = document.getElementById('img-translated');
const downloadImgBtn = document.getElementById('download-img-btn');

let currentImgFile = null;
let downloadImgUrl = null;

imgUploadArea.addEventListener('click', () => {
    imgFileInput.click();
});

imgUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    imgUploadArea.style.borderColor = 'var(--secondary-color)';
});

imgUploadArea.addEventListener('dragleave', () => {
    imgUploadArea.style.borderColor = 'var(--border-color)';
});

imgUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    imgUploadArea.style.borderColor = 'var(--border-color)';

    const file = e.dataTransfer.files[0];
    if (file) {
        handleImgFile(file);
    }
});

imgFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleImgFile(file);
    }
});

function handleImgFile(file) {
    currentImgFile = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        imgPreview.innerHTML = `<img src="${e.target.result}" alt="Preview" style="max-width: 100%; max-height: 400px; border-radius: 8px;">`;
    };
    reader.readAsDataURL(file);

    imgUploadArea.style.display = 'none';
    imgFileInfo.style.display = 'block';
    imgResult.style.display = 'none';
}

translateImgBtn.addEventListener('click', async () => {
    if (!currentImgFile) return;

    const formData = new FormData();
    formData.append('file', currentImgFile);
    formData.append('source_lang', document.getElementById('img-source-lang').value);
    formData.append('target_lang', document.getElementById('img-target-lang').value);

    translateImgBtn.disabled = true;
    imgFileInfo.style.display = 'none';
    imgProgress.style.display = 'block';

    // Simulate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 5;
        if (progress >= 90) {
            clearInterval(progressInterval);
        }
        imgProgressFill.style.width = progress + '%';
    }, 500);

    try {
        const response = await fetch('/api/translate-image', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        clearInterval(progressInterval);
        imgProgressFill.style.width = '100%';

        if (response.ok) {
            downloadImgUrl = data.download_url;

            // Show comparison
            const reader = new FileReader();
            reader.onload = (e) => {
                imgOriginal.src = e.target.result;
            };
            reader.readAsDataURL(currentImgFile);

            imgTranslated.src = data.preview_url;

            imgProgress.style.display = 'none';
            imgResult.style.display = 'block';
        } else {
            alert('Translation error: ' + data.error);
            imgFileInfo.style.display = 'block';
            imgProgress.style.display = 'none';
        }
    } catch (error) {
        clearInterval(progressInterval);
        alert('Network error: ' + error.message);
        imgFileInfo.style.display = 'block';
        imgProgress.style.display = 'none';
    } finally {
        translateImgBtn.disabled = false;
    }
});

downloadImgBtn.addEventListener('click', () => {
    if (downloadImgUrl) {
        window.location.href = downloadImgUrl;
    }
});

// Helper Functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Auto-detect language on input
let detectTimeout;
sourceText.addEventListener('input', () => {
    clearTimeout(detectTimeout);

    const text = sourceText.value.trim();

    if (text.length > 10 && sourceLang.value === 'auto') {
        detectTimeout = setTimeout(async () => {
            try {
                const response = await fetch('/api/detect-language', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: text })
                });

                const data = await response.json();

                if (response.ok) {
                    detectedLang.textContent = `Detected: ${data.language_name} (${Math.round(data.confidence * 100)}%)`;
                }
            } catch (error) {
                console.error('Language detection error:', error);
            }
        }, 1000);
    } else {
        detectedLang.textContent = '';
    }
});
