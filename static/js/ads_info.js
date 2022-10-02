const firsCategoryBtn = document.getElementById("firstCategoryBtn")
const firsCategoryModal = document.getElementById("firstCategoryModal")
const closeModal = document.querySelector(".modal-close")
const allCategoryModal = document.querySelector('.modal-container')

firsCategoryBtn.addEventListener('click', function (){
    firsCategoryModal.classList.add("active");
})

closeModal.addEventListener('click', function (){
    allCategoryModal.classList.remove('active');
})