const swiper = new Swiper(".swiper", {
    effect: "fade",
    pagination: {
        el: ".swiper-pagination",
    },
    autoplay: {
        delay: 2000,
        disableOnInteraction: false,
    },
});

let phoneInput = document.querySelector('#phone_number');

phoneInput.addEventListener('focus', () => {
  if (phoneInput.value === '') {
    phoneInput.value = '+7 ';
  }
});

phoneInput.addEventListener('input', () => {
  let rawValue = phoneInput.value.replace(/\D/g, '');
  
  if (!rawValue.startsWith('7')) {
    rawValue = '7' + rawValue;
  }

  let formattedValue = '+7 ';
  if (rawValue.length > 1) formattedValue += '(' + rawValue.substring(1, 4);
  if (rawValue.length >= 4) formattedValue += ') ' + rawValue.substring(4, 7);
  if (rawValue.length >= 7) formattedValue += '-' + rawValue.substring(7, 9);
  if (rawValue.length >= 9) formattedValue += '-' + rawValue.substring(9, 11);

  phoneInput.value = formattedValue;
});

phoneInput.addEventListener('keypress', (e) => {
  if (!/\d/.test(e.key)) {
    e.preventDefault();
  }
});

function displayFileNameAR() {
    const fileInput = document.getElementById('ar_file');
    const fileNameElement = document.getElementById('ar_file_name');
    const fileName = fileInput.files[0] ? fileInput.files[0].name : '';
    
    if (fileName) {
        fileNameElement.textContent = fileName;
        fileNameElement.style.display = 'block'; // Показываем текст при наличии имени файла
    } else {
        fileNameElement.style.display = 'none'; // Скрываем элемент, если файла нет
    }
}

function displayFileNamePhoto() {
    const fileInput = document.getElementById('photo_file');
    const fileNameElement = document.getElementById('photo_file_name');
    const fileName = fileInput.files[0] ? fileInput.files[0].name : '';
    
    if (fileName) {
        fileNameElement.textContent = fileName;
        fileNameElement.style.display = 'block'; // Показываем текст при наличии имени файла
    } else {
        fileNameElement.style.display = 'none'; // Скрываем элемент, если файла нет
    }
}

function validateNumberInput(input) {
    // Разрешаем ввод только чисел и одной точки
    input.value = input.value.replace(/[^0-9.]/g, '');

    // Удаляем все точки, кроме первой, если их больше одной
    const parts = input.value.split('.');
    if (parts.length > 2) {
        input.value = parts[0] + '.' + parts.slice(1).join('');
    }
}
