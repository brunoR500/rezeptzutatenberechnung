/**
 * Calculates the ingredients of the given recipes
 *
 * @param {Object} recipes
 * @returns {Object} ingredients
 */
function calculateIngredients(recipes) {
	let ingredients = {};
	Object.values(recipes).forEach((recipe) => {
		recipe.ingredients.forEach((ingredient) => {
			// converts the unit into one base unit to calculate with
			switch (ingredient.unit) {
				case "kg":
					ingredient.quantity *= 1000;
					ingredient.unit = "g";
					break;
				case "l":
					ingredient.quantity *= 1000;
					ingredient.unit = "ml";
					break;
			}
			const identifier = ingredient.name + ingredient.unit;
			const quantity = parseFloat(ingredient.quantity) * recipe.portions;
			if (identifier in ingredients) {
				ingredients[identifier]["quantity"] += quantity;
			} else {
				ingredients[identifier] = {};
				ingredients[identifier]["name"] = ingredient.name;
				ingredients[identifier]["unit"] = ingredient.unit;
				ingredients[identifier]["quantity"] = quantity;
			}
		});
	});

	// converts the unit back
	Object.values(ingredients).forEach((ingredient) => {
		if (ingredient.quantity >= 1000) {
			ingredient.quantity /= 1000;
			switch (ingredient.unit) {
				case "g":
					ingredient.unit = "kg";
					break;
				case "ml":
					ingredient.unit = "l";
					break;
			}
		}
		ingredient.quantity = ingredient.quantity.toFixed(2);
	});

	return Object.entries(ingredients)
		.sort()
		.map((ingredient) => ingredient[1]);
}

/**
 * Inserts a new recipe into the table, containing the id as an identifier of the row
 *
 * @param {string} id
 * @param {string} name
 */
function insertRecipe(id, name, portions) {
	const html = `
                <tr>
                    <td class="align-middle">${name}</td>
                    <td id="${id}" class="align-middle">
                        <input
                            value=${portions}
                            type="number"
                            id="portions"
                            name="portions"
                            min="1"
                            max="100"
                        />
                    </td>
                    <td id="${id}" class="align-middle">
                        <button type="button" class="btn btn-danger">Löschen</button>
                    </td>
                </tr>
                `;

	document.getElementById("recipeTable").insertRow(-1).innerHTML = html;
}

/**
 * Inserts a new ingredient into the table
 *
 * @param {string} name
 * @param {string} quantity
 * @param {string} unit
 */
function insertIngredient(name, quantity, unit) {
	const html = `
                <tr>
                    <td class="align-middle">${name}</td>
                    <td class="align-middle">${quantity}</td>
                    <td class="align-middle">${unit}</td>
                </tr>
                `;

	document.getElementById("ingredientsTable").insertRow(-1).innerHTML = html;
}

/* Updates the ingredients table with the new values */
function updateIngredientTable() {
	$("#ingredientsTable tr").remove();
	calculateIngredients(getRecipes()).forEach((ingredient) => {
		insertIngredient(ingredient.name, ingredient.quantity, ingredient.unit);
	});
}

/* on addButton clicked get the recipe data if they exist */
document.getElementById("addButton").addEventListener("click", () => {
	const search = document.getElementById("searchfield").value;
	if (search !== "") {
		fetch("/api/recipe/" + search)
			.then((res) => res.json())
			.then((data) => {
				if (data.detail) {
					document.getElementById("notFound").style.visibility = "visible";
				} else {
					document.getElementById("notFound").style.visibility = "hidden";
					addRecipe(data).then((added) => {
						if (added) {
							insertRecipe(data.id, data.name, 1);
							updateIngredientTable();
						}
					});
				}
			})
			.catch((err) => console.error(err));
	}
});

/* on delete button clicked remove the recipe */
$("#recipeTable").on("click", ".btn-danger", function () {
	removeRecipeById($(this).closest("td").attr("id"));
	$(this).closest("tr").remove();
	updateIngredientTable();
});

/* on portions value changed update the portions in the storage and update ingredients table*/
$("#recipeTable").on("input", "#portions", function () {
	changePortionsById($(this).closest("td").attr("id"), $(this).val());
	updateIngredientTable();
});

/* init the page */
$(document).ready(function () {
	Object.values(getRecipes()).forEach((recipe) =>
		insertRecipe(recipe.id, recipe.name, recipe.portions),
	);
	updateIngredientTable();
	fetch("/api/recipes/")
		.then((res) => res.json())
		.then((recipes) => {
			autocomplete(
				document.getElementById("searchfield"),
				Object.values(recipes).map((recipe) => recipe.name),
			);
		})
		.catch((err) => console.error(err));
});
