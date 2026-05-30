const accountBehavior = {
  deposit(amount) {
    if (!Number.isFinite(amount) || amount <= 0) {
      throw new RangeError("deposit amount must be positive");
    }
    this.balance += amount;
    return this.balance;
  },
  describe() {
    return `${this.owner}: $${this.balance}`;
  },
};

function createAccount(owner, openingBalance) {
  const account = Object.create(accountBehavior);
  account.owner = owner;
  account.balance = openingBalance;
  return account;
}

const checking = createAccount("Ada", 100);
const savings = createAccount("Grace", 250);

checking.deposit(25);
savings.deposit(50);

console.log("checking", checking.describe());
console.log("savings", savings.describe());
console.log("checking owns deposit", Object.hasOwn(checking, "deposit"));
console.log("prototype match", Object.getPrototypeOf(checking) === accountBehavior);

checking.describe = function describeCheckingOnly() {
  return `${this.owner} checking balance is $${this.balance}`;
};

console.log("checking shadowed", checking.describe());
console.log("savings shared", savings.describe());
console.log("checking owns describe", Object.hasOwn(checking, "describe"));

try {
  const detachedDeposit = checking.deposit;
  detachedDeposit(10);
} catch (error) {
  console.log("detached method error", error.message);
}
