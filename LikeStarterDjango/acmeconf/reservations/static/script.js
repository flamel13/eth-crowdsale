function my_toggle_func() {
        if (this.checked) {
                document.getElementById("prova").style.display = 'block';
        } else {
                document.getElementById("prova").style.display = 'none';
        }
}

document.getElementById('is_staff').onclick = my_toggle_func;
