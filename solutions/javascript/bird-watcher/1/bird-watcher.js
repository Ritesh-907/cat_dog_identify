// @ts-check
//
// The line above enables type checking for this file. Various IDEs interpret
// the @ts-check directive. It will give you helpful autocompletion when
// implementing this exercise.

/**
 * Calculates the total bird count.
 *
 * @param {number[]} birdsPerDay
 * @returns {number} total bird count
 */
export function totalBirdCount(birdsPerDay) {
  let count=0
   for (let i = 0; i < birdsPerDay.length; i++) {
     count += birdsPerDay[i];
   }
  return count
}

/**
 * Calculates the total number of birds seen in a specific week.
 *
 * @param {number[]} birdsPerDay
 * @param {number} week
 * @returns {number} birds counted in the given week
 */
export function birdsInWeek(birdsPerDay, week) {
  let i =1;
  let j=0;
  let k=0;
  const countPerWeek = [];
  for (i; i <= week; i++) {
    k = i * 7
    j = 7 * (i-1)
    let count = 0;
    for (j; j < k; j++) {
      count += birdsPerDay[j]
    }
      countPerWeek.push(count)
      count = 0;
  }
  return countPerWeek[week-1]
}

/**
 * Fixes the counting mistake by increasing the bird count
 * by one for every second day.
 *
 * @param {number[]} birdsPerDay
 * @returns {void} should not return anything
 */
export function fixBirdCountLog(birdsPerDay) {
  for (let i = 0; i < birdsPerDay.length; i++) {
    if (i % 2 === 0) {
      birdsPerDay[i] += 1;
    }
  }
}
