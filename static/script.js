function downloadPDF() {
  const element = document.getElementById('receipt-content');
  const btn = document.querySelector('button[onclick="downloadPDF()"]');
  if (btn) btn.style.display = 'none';

  // Temporarily remove background for PDF clarity
  const originalBg = document.body.style.background;
  document.body.style.background = '#fff';

  const opt = {
    margin: 0,
    filename: 'SustainaBill-Receipt.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 1, useCORS: true, scrollY: 0 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
    pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
  };
  html2pdf().set(opt).from(element).save().then(() => {
    if (btn) btn.style.display = '';
    document.body.style.background = originalBg;
  });
}

function sendPDFToEmail() {
  const element = document.getElementById('receipt-content');
  const btn = document.querySelector('button[onclick="sendPDFToEmail()"]');
  if (btn) btn.disabled = true;

  const opt = {
    margin: 0,
    filename: 'SustainaBill-Receipt.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 1, useCORS: true, scrollY: 0 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
    pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
  };

  html2pdf().set(opt).from(element).outputPdf('blob').then(function(pdfBlob) {
    const formData = new FormData();
    formData.append('pdf', pdfBlob);

    fetch('/send_receipt_pdf', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(msg => {
      alert(msg);
      if (btn) btn.disabled = false;
    })
    .catch(err => {
      alert('Failed to send email: ' + err);
      if (btn) btn.disabled = false;
    });
  });
}

// Text-to-Speech functionality
let speechSynthesis = window.speechSynthesis;
let currentUtterance = null;
let isReading = false;
let voicesLoaded = false;

function ensureVoicesLoaded(callback) {
  let voices = speechSynthesis.getVoices();
  if (voices.length !== 0) {
    voicesLoaded = true;
    callback();
  } else {
    speechSynthesis.onvoiceschanged = () => {
      voicesLoaded = true;
      callback();
    };
  }
}

function readReceipt() {
  const readBtn = document.getElementById('readBtn');
  if (isReading) {
    if (currentUtterance) {
      speechSynthesis.cancel();
    }
    isReading = false;
    readBtn.textContent = '🔊 Read Receipt';
    readBtn.classList.remove('playing');
    return;
  }
  ensureVoicesLoaded(() => {
    const receiptText = generateReceiptText();
    console.log('Text to read:', receiptText);
    if (!receiptText || receiptText.trim().length === 0) {
      alert("Nothing to read in the receipt!");
      return;
    }
    if (speechSynthesis.speaking) {
      speechSynthesis.cancel();
    }
    currentUtterance = new SpeechSynthesisUtterance(receiptText);
    currentUtterance.rate = 0.9;
    currentUtterance.pitch = 1.0;
    currentUtterance.volume = 1.0;
    const voices = speechSynthesis.getVoices();
    if (voices.length > 0) {
      currentUtterance.voice = voices[0]; // Use the first available voice
    }
    currentUtterance.onstart = function() {
      isReading = true;
      readBtn.textContent = '⏹️ Stop Reading';
      readBtn.classList.add('playing');
    };
    currentUtterance.onend = function() {
      isReading = false;
      readBtn.textContent = '🔊 Read Receipt';
      readBtn.classList.remove('playing');
    };
    currentUtterance.onerror = function(event) {
      console.error('Speech synthesis error:', event);
      isReading = false;
      readBtn.textContent = '🔊 Read Receipt';
      readBtn.classList.remove('playing');
      alert('Speech synthesis not supported or failed. Please try again.');
    };
    speechSynthesis.speak(currentUtterance);
  });
}

function generateReceiptText() {
  const customerInfo = document.querySelector('.customer-info');
  let customerName = '', customerContact = '';
  if (customerInfo) {
    const strongs = customerInfo.querySelectorAll('strong');
    if (strongs.length >= 2) {
      customerName = strongs[0].nextSibling ? strongs[0].nextSibling.textContent.trim() : '';
      customerContact = strongs[1].nextSibling ? strongs[1].nextSibling.textContent.trim() : '';
    }
  }

  let text = `Eco Receipt. `;
  text += `Customer: ${customerName}. Contact: ${customerContact}. `;

  // Read items
  const itemsTable = document.querySelector('.receipt-table');
  if (itemsTable) {
    const items = itemsTable.querySelectorAll('tbody tr');
    text += `Items purchased: `;
    items.forEach((item, index) => {
      const cells = item.querySelectorAll('td');
      if (cells.length >= 7) {
        const itemName = cells[0].textContent.trim();
        const quantity = cells[1].textContent.trim();
        const price = cells[2].textContent.trim();
        const total = cells[3].textContent.trim();
        const carbon = cells[4].textContent.trim();
        const recyclable = cells[5].textContent.trim();
        const ethical = cells[6].textContent.trim();
        text += `${index + 1}. ${itemName}, quantity: ${quantity}, price: ${price}, total: ${total}, CO2: ${carbon}, recyclable: ${recyclable}, ethical score: ${ethical}. `;
      }
    });
  }

  // Read summary
  const summary = document.querySelector('.summary');
  if (summary) {
    text += summary.textContent.trim() + '. ';
  }

  // Read info box
  const infoBox = document.querySelector('.info-box');
  if (infoBox) {
    text += 'Note: ' + infoBox.textContent.trim() + '. ';
  }

  return text;
}

// Initialize speech synthesis when page loads
document.addEventListener('DOMContentLoaded', function() {
  // Load voices if they're not immediately available
  if (speechSynthesis.getVoices().length === 0) {
    speechSynthesis.addEventListener('voiceschanged', function() {
      console.log('Voices loaded:', speechSynthesis.getVoices().length);
    });
  }
});

// Theme toggle functionality
function toggleTheme() {
  document.body.classList.toggle('dark-theme');
  const btn = document.getElementById('themeToggleBtn');
  if (document.body.classList.contains('dark-theme')) {
    btn.innerHTML = '🌞 Light Theme';
  } else {
    btn.innerHTML = '🌓 Dark Theme';
  }
}