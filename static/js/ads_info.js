const firsCategoryBtn = document.getElementById("firstCategoryBtn")
const firsCategoryModal = document.getElementById("firstCategoryModal")
const secondCategoryModal = document.getElementById("secondCategoryModal")
const thirdCategoryModal = document.getElementById("thirdCategoryModal")
const fourCategoryModal = document.getElementById("fourCategoryModal")
const fiveCategoryModal = document.getElementById("fiveCategoryModal")
const closeModal = document.querySelectorAll(".modal-close")
const allCategoryModal = document.querySelectorAll('.modal-container')
const secondCategoryBtn = document.querySelectorAll('.secondCategoryBtn')
const thirdCategoryBtn = document.querySelector('.thirdCategoryBtn')
const fourCategoryBtn = document.querySelector('.fourCategoryBtn')
const fiveCategoryBtn = document.querySelector('.fiveCategoryBtn')

firsCategoryBtn.addEventListener('click', function () {
    firsCategoryModal.classList.add("active");
})


secondCategoryBtn.forEach(btn => {
    btn.addEventListener('click', function () {
        secondCategoryModal.classList.add("active")
    })
})

thirdCategoryBtn.addEventListener('click', function (){
    thirdCategoryModal.classList.add('active')
})

fourCategoryBtn.addEventListener('click', function (){
    fourCategoryModal.classList.add('active')
})

fiveCategoryBtn.addEventListener('click', function (){
    fiveCategoryModal.classList.add('active')
})

closeModal.forEach(btn => {
    btn.addEventListener('click', function () {
        allCategoryModal.forEach(i => {
            i.classList.remove("active")
        })
    })
})

