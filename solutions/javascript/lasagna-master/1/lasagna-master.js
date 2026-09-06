/// <reference path="./global.d.ts" />
// @ts-check

/**
 * Implement the functions needed to solve the exercise here.
 * Do not forget to export them so they are available for the
 * tests. Here an example of the syntax as reminder:
 *
 * export function yourFunction(...) {
 *   ...
 * }
 */
export function cookingStatus(timer) {
  if(timer === undefined) return 'You forgot to set the timer.'
  if(timer===0) return 'Lasagna is done.'
  return 'Not done, please wait.'
}

export function preparationTime(layer,time){
  if(time === undefined){
    return 2 * layer.length
  }
  else{
    return time * layer.length
  }
}
export function quantities(layer){
  let noodlesCount = 0;
  let sauceCount = 0;
  for (let item of layer){
    if(item==='noodles') noodlesCount+=50;
    else if (item === 'sauce') sauceCount+=0.2;
  }
  return {'noodles':noodlesCount,"sauce":sauceCount};
}

export function addSecretIngredient(friendList,myList) {
  myList.push(friendList[friendList.length-1]);
}
export function scaleRecipe(recipe,scale){
   // Calculate the multiplier based on the original 2 portions
  const factor = scale / 2;
  
  // Create an empty object for the scaled recipe
  const scaledRecipe = {};

  // Loop through each ingredient and multiply the amount
  for (const ingredient in recipe) {
    scaledRecipe[ingredient] = recipe[ingredient] * factor;
  }

  return scaledRecipe;
}
