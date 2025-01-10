// Загрузка фильтров (авторов и категорий) при запуске страницы
function loadFilters() {
    const authorSelect = document.getElementById('author-select');
    const categorySelect = document.getElementById('category-select');
    authorSelect.innerHTML = '<option value="">Select an author</option>';
    categorySelect.innerHTML = '<option value="">Select a category</option>';

    fetch('/get_authors')
        .then(response => response.json())
        .then(data => {
            const authorSelect = document.getElementById('author-select');
            data.forEach(author => {
                const option = document.createElement('option');
                option.value = author;
                option.textContent = author;
                authorSelect.appendChild(option);
            });
        });

    fetch('/get_categories')
        .then(response => response.json())
        .then(data => {
            const categorySelect = document.getElementById('category-select');
            data.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categorySelect.appendChild(option);
            });
        });
}

// Получение случайной цитаты из базы данных
function getRandomQuote() {
    fetch('/get_random_quote')
        .then(response => response.json())
        .then(data => {
            document.getElementById('quote-text').innerText = data.text;
            document.getElementById('quote-author').innerText = `- ${data.author}`;
        });
}

// Получение случайной цитаты из внешнего API
function getExternalQuote() {
    fetch('/get_external_quote')
        .then(response => response.json())
        .then(data => {
            document.getElementById('quote-text').innerText = data.text;
            document.getElementById('quote-author').innerText = `- ${data.author}`;
        });
}

// Добавление новой цитаты
document.getElementById('add-quote-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = {
        text: document.getElementById('text').value,
        author: document.getElementById('author').value,
        category: document.getElementById('category').value
    };

    fetch('/add_quote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert('Quote added successfully!');
        document.getElementById('add-quote-form').reset();
        loadFilters(); // Обновляем фильтры после добавления новой цитаты
    })
    .catch(error => console.error('Error:', error));
});

// Сортировка цитат по автору
function sortByAuthor() {
    const author = document.getElementById('author-select').value;
    if (!author) {
        alert('Please select an author.');
        return;
    }
    fetch(`/get_quotes_by_author/${author}`)
        .then(response => response.json())
        .then(data => {
            displayQuotes(data);
        });
}

// Сортировка цитат по категории
function sortByCategory() {
    const category = document.getElementById('category-select').value;
    if (!category) {
        alert('Please select a category.');
        return;
    }
    fetch(`/get_quotes_by_category/${category}`)
        .then(response => response.json())
        .then(data => {
            displayQuotes(data);
        });
}

// Отображение цитат
function displayQuotes(quotes) {
    const quoteList = document.getElementById('quote-list');
    quoteList.innerHTML = '<h3>Quotes:</h3>';
    quotes.forEach(quote => {
        const quoteDiv = document.createElement('div');
        quoteDiv.innerHTML = `<p>"${quote.text}" - ${quote.author} (${quote.category})</p>`;
        quoteList.appendChild(quoteDiv);
    });
}

// Загрузка фильтров при загрузке страницы
window.onload = loadFilters;