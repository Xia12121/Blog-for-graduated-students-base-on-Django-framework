function search() {
    let input = document.getElementById("searchInput");
    let filter = input.value.toUpperCase();
    let ul = document.getElementById("searchList");
    let li = ul.getElementsByTagName("li");

    for (let i = 0; i < li.length; i++) {
        let txtValue = li[i].textContent || li[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function toggleDropdown(show) {
    let ul = document.getElementById("searchList");
    if (show) {
        ul.classList.add("visible");
    } else {
        ul.classList.remove("visible");
    }
}

function selectItem(item) {
    let input = document.getElementById("searchInput");
    input.value = item.innerHTML;
    toggleDropdown(false);
}