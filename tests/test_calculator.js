import assert from 'assert';
import { calculateDistanceMeters, computeDeliveryFee, computeOrderBreakdown } from '../js/calculator.js';
import { INITIAL_PRODUCTS } from '../js/data.js';

console.log("🧪 Lancement des tests unitaires de GazExpress...");

// Test 1: Calcul de distance
const coto1 = { lat: 6.3685, lng: 2.4512 };
const coto2 = { lat: 6.3541, lng: 2.3986 };
const dist = calculateDistanceMeters(coto1.lat, coto1.lng, coto2.lat, coto2.lng);
console.log(`- Distance Akpakpa -> Haie Vive: ${dist} m`);
assert(dist > 5000 && dist < 7000, "Distance calculée incorrecte");

// Test 2: Règle de tarification 6kg
// - <= 500m -> 500f
const f6_300 = computeDeliveryFee(300, "6kg");
assert.strictEqual(f6_300.deliveryFee, 500);
assert.strictEqual(f6_300.driverPayout, 500);
assert.strictEqual(f6_300.companyDeliveryMargin, 0);

// - 1000m -> 1000f
const f6_1000 = computeDeliveryFee(1000, "6kg");
assert.strictEqual(f6_1000.deliveryFee, 1000);
assert.strictEqual(f6_1000.driverPayout, 500);
assert.strictEqual(f6_1000.companyDeliveryMargin, 500);

// - 1200m (comme demandé explicitement par l'utilisateur: "1.,2 km=1500f")
const f6_1200 = computeDeliveryFee(1200, "6kg");
assert.strictEqual(f6_1200.deliveryFee, 1500);
assert.strictEqual(f6_1200.driverPayout, 500);
assert.strictEqual(f6_1200.companyDeliveryMargin, 1000);

// - 1500m -> 1500f
const f6_1500 = computeDeliveryFee(1500, "6kg");
assert.strictEqual(f6_1500.deliveryFee, 1500);

// - 1600m -> 2000f
const f6_1600 = computeDeliveryFee(1600, "6kg");
assert.strictEqual(f6_1600.deliveryFee, 2000);

// Test 3: Règle de tarification 12.5kg
// - <= 500m -> 700f
const f12_400 = computeDeliveryFee(400, "12.5kg");
assert.strictEqual(f12_400.deliveryFee, 700);
assert.strictEqual(f12_400.driverPayout, 500);
assert.strictEqual(f12_400.companyDeliveryMargin, 200);

// - 1000m -> 1400f
const f12_1000 = computeDeliveryFee(1000, "12.5kg");
assert.strictEqual(f12_1000.deliveryFee, 1400);

// - 1200m -> 2100f
const f12_1200 = computeDeliveryFee(1200, "12.5kg");
assert.strictEqual(f12_1200.deliveryFee, 2100);

// Test 4: Dispatching des montants
const b6 = INITIAL_PRODUCTS.find(p => p.id === "B6_RECHARGE");
const breakdown = computeOrderBreakdown(b6, 1200);
assert.strictEqual(breakdown.gasPrice, 4950);
assert.strictEqual(breakdown.deliveryFee, 1500);
assert.strictEqual(breakdown.totalCustomerToPay, 6450);
assert.strictEqual(breakdown.dispatching.depotAmount, 4450);
assert.strictEqual(breakdown.dispatching.driverAmount, 500);
assert.strictEqual(breakdown.dispatching.companyGasMargin, 500);
assert.strictEqual(breakdown.dispatching.companyDeliveryMargin, 1000);
assert.strictEqual(breakdown.dispatching.totalCompanyMargin, 1500);

// Vérification de la somme d'équilibre comptable
const totalDistributed = breakdown.dispatching.depotAmount + breakdown.dispatching.driverAmount + breakdown.dispatching.totalCompanyMargin;
assert.strictEqual(totalDistributed, breakdown.totalCustomerToPay, "L'équilibre comptable du dispatching est faussé");

console.log("✅ Tous les tests de calcul et de modélisation sont validés avec succès !");
