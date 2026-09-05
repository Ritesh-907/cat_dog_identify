// @ts-check

/**
 * Determine how many cards of a certain type there are in the deck
 *
 * @param {number[]} stack
 * @param {number} card
 *
 * @returns {number} number of cards of a single type there are in the deck
 */
export function cardTypeCheck(stack, card) {
  // 🚨 Use .forEach
  let count = 0;
  stack.forEach(function(n) {
    if(n === card ) count ++
  })
  return count
}

/**
 * Determine how many cards are odd or even
 *
 * @param {number[]} stack
 * @param {boolean} type the type of value to check for - odd or even
 * @returns {number} number of cards that are either odd or even (depending on `type`)
 */
export function determineOddEvenCards(stack, type) {
 const arrOdd = []
  const arrEven = []
  for (let n of stack) {
    if(n%2!=0){
      arrOdd.push(n)
    }
    else if(n%2 === 0){
      arrEven.push(n)
    }
    
  }
    if(!type) return arrOdd.length;
    if(type) return arrEven.length;
}