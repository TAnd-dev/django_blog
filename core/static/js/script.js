let sorts = document.getElementsByClassName('dropdown-item')
for (let sort of sorts) {
    if (sort == window.location.href){
        sort.classList.add("active")
    }
}



