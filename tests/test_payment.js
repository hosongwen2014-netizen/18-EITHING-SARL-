import assert from 'assert';
import { PaymentGateway } from '../js/payment.js';

console.log("🧪 Tests de la passerelle de paiement MoMo & Banques...");

const gw = new PaymentGateway();

// Test MTN
const mtnOk = gw.validatePhoneNumber("97 11 22 33", "mtn_momo");
assert.strictEqual(mtnOk.valid, true);
assert.strictEqual(mtnOk.cleanedPhone, "97112233");

const mtnFail = gw.validatePhoneNumber("95 11 22 33", "mtn_momo");
assert.strictEqual(mtnFail.valid, false);

// Test Moov
const moovOk = gw.validatePhoneNumber("95 44 55 66", "moov_money");
assert.strictEqual(moovOk.valid, true);

// Test Celtiis
const celtiisOk = gw.validatePhoneNumber("+229 40 12 34 56", "celtiis_cash");
assert.strictEqual(celtiisOk.valid, true);

// Test Virement bancaire
const dummyOrders = [
  { totalCustomerToPay: 6450, dispatching: { depotAmount: 4450, driverAmount: 500, totalCompanyMargin: 1500 } },
  { totalCustomerToPay: 12400, dispatching: { depotAmount: 9300, driverAmount: 500, totalCompanyMargin: 2600 } }
];
const payoutOrder = gw.generateBankPayoutOrder(dummyOrders);
assert.strictEqual(payoutOrder.summary.totalCollected, 18850);
assert.strictEqual(payoutOrder.summary.totalDepotRevenue, 13750);
assert.strictEqual(payoutOrder.summary.totalDriverPayouts, 1000);
assert.strictEqual(payoutOrder.summary.totalCompanyRevenue, 4100);

console.log("✅ Tests de la passerelle MoMo et Bancaire validés !");
