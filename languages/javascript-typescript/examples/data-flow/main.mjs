const courses = [
  { name: "promises", minutes: 25 },
  { name: "modules", minutes: 35 },
];

const total = courses.reduce((sum, item) => sum + item.minutes, 0);
console.log(`total minutes = ${total}`);
