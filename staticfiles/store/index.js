function showProfile(){
   let box= document.getElementById("profiles");
    box.style.display = (box.style.display === "block") ? "none" : "block";
}



document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('search-box');
    const suggestionsList = document.getElementById('suggestions-list');
    const suggestUrl = input.form.getAttribute('data-suggest-url');

    //console.log("Suggest URL:", suggestUrl); // now this will work

    input.addEventListener('input', function () {
        const query = this.value;
        if (query.length < 2) {
            suggestionsList.innerHTML = '';
            return;
        }

        fetch(`${suggestUrl}?q=${encodeURIComponent(query)}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            suggestionsList.innerHTML = '';
            data.suggestions.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                li.onclick = () => {
                    input.value = item;
                    suggestionsList.innerHTML = '';
                    input.form.submit();
                };
                suggestionsList.appendChild(li);
            });
        })
        .catch(err => console.error("Error fetching suggestions:", err));
    });
});
// mobile search and suggestions
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('search-boxmobile');
    const suggestionsList = document.getElementById('suggestions-listmobile');
    const suggestUrl = input.form.getAttribute('data-suggest-url');

    //console.log("Suggest URL:", suggestUrl); // now this will work

    input.addEventListener('input', function () {
        const query = this.value;
        if (query.length < 2) {
            suggestionsList.innerHTML = '';
            return;
        }

        fetch(`${suggestUrl}?q=${encodeURIComponent(query)}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            suggestionsList.innerHTML = '';
            data.suggestions.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                li.onclick = () => {
                    input.value = item;
                    suggestionsList.innerHTML = '';
                    input.form.submit();
                };
                suggestionsList.appendChild(li);
            });
        })
        .catch(err => console.error("Error fetching suggestions:", err));
    });
});


  /*document.getElementById('chat-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;

    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
    input.value = '';

    fetch("{% url 'ecommerce_bot' %}", {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.innerHTML += `<p><strong>Dan:</strong> ${data.reply}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(err => {
        chatBox.innerHTML += `<p style="color:red;"><strong>Error:</strong> Could not reach Dan</p>`;
    });
}); */

/*function addToCart(productId) {
    const csrftoken = document.getElementById("csrf").value;

    fetch(`/cart/add/${productId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Update cart count in navbar (if you have one)
            let cartCount = document.getElementById("cart-count");
            if (cartCount) {
                cartCount.innerText = data.cart_count;
            }
            // 👇 no alert, just update quietly
            console.log(data.message);
        }
    });
}
    */
   document.querySelectorAll('.filter-input').forEach(input => {
    input.addEventListener('change', () => {
        const form = document.getElementById('filter-form');
        const formData = new FormData(form);
        const queryString = new URLSearchParams(formData).toString();

        fetch(`/search/?${queryString}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(res => res.text())
        .then(html => {
            document.getElementById('product-grid').innerHTML = html;
        });
    });
});
