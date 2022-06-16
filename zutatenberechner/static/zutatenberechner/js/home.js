/* Get the recipes of the clicked card and add them to the storage */
$(".stretched-link").click(function () {
	fetch("/api/card/" + $(this).attr("id"))
		.then((res) => res.json())
		.then((recipes) => {
			const promises = [];
			recipes.forEach((recipe) => promises.push(addRecipe(recipe)));
			Promise.all(promises).then(() => (window.location.href = "berechner"));
		})
		.catch((err) => console.error(err));
});
