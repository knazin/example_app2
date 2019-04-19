window.onload = function() {
    ShowRecipes()
    ShowDepots()
    ShowCoffe()   
}

function ShowRecipes() {
    let recipes = data.recipes

    recipes.forEach(v => {
        let div = document.createElement('div')
        div.style = null
        div.classList.add('col')
        div.classList.add('col-coffe')
        div.id = v.recipe_name
        div.innerHTML = v.recipe_name

        div.addEventListener('click', function() {
            document.getElementById('message').innerHTML = `Selected ${v.recipe_name}`
            
            // show the submit button
            document.getElementById('submit').type = 'submit'
            let input = document.getElementById('drink')
            input.value = v.recipe_name
        })

        document.getElementById('coffe').appendChild(div)
    })
}

function ShowDepots() {
    let ingredients = data.ingredients

    ingredients.forEach(v => {
        let div = document.createElement('li')
        div.classList.add('list-group-item')
        div.classList.add('ingredient')
        div.innerHTML = `${v.ingredient_name} <br> ${v.capacity} ml`
        document.getElementById('ingredient-list').appendChild(div)
    })
}

function ShowCoffe() {
    let photopath = data.photo
    let img = document.getElementById("imgClickAndChange")
    
    if (photopath != '../static/img/') {
        img.style.visibility = 'visible'
        img.src = `../static/img/${photopath}`;
    } else {
        img.style.visibility = 'hidden'
    }

    document.getElementById('message').innerHTML = data.message
}