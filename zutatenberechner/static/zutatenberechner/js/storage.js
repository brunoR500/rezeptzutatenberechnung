/**
 * @returns {Object} Recipes in the storage
 */
function getRecipes() {
	/* Creates a new empty dictionary if recipes is null (visited first time) */
	if (sessionStorage.getItem("recipes") === null) {
		saveRecipes({});
	}
	return JSON.parse(sessionStorage.getItem("recipes"));
}

/**
 * Stores the whole given object into the storage
 *
 * @param {Object} recipes - Recipes which to store
 */
function saveRecipes(recipes) {
	sessionStorage.setItem("recipes", JSON.stringify(recipes));
}

/**
 * Removes the recipe, identified by id
 *
 * @param {number} id - Id of the recipe to remove
 */
function removeRecipeById(id) {
	const recipes = getRecipes();
	delete recipes[id];
	saveRecipes(recipes);
}

function changePortionsById(id, portions) {
	const recipes = getRecipes();
	Object.values(recipes).forEach((recipe) => {
		if (recipe.id == id) {
			recipe.portions = portions;
		}
	});
	saveRecipes(recipes);
}

/**
 * Adds the given recipe if its a new one and returns whether it was added
 *
 * @param {Object} newRecipe - The new recipe which should be added
 * @returns {boolean} The boolean whether the object was added
 */
async function addRecipe(newRecipe) {
	return fetch("/api/ingredients/" + newRecipe.id)
		.then((res) => res.json())
		.then((ingredients) => {
			if (newRecipe.id in getRecipes()) {
				return false;
			}
			const recipes = getRecipes();
			newRecipe.ingredients = ingredients;
			newRecipe.portions = 1;
			recipes[newRecipe.id] = newRecipe;
			saveRecipes(recipes);
			return true;
		})
		.catch((err) => {
			console.error(err);
			return false;
		});
}
