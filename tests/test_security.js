import assert from 'assert';
import { SecurityManager } from '../js/security.js';

console.log("🧪 Tests du module de Sécurité Anti-Fraude & Anti-Hacking...");

// Test 1: Génération de code OTP 4 chiffres
const otp = SecurityManager.generateDeliveryOTP();
assert(/^[0-9]{4}$/.test(otp), "Le code OTP doit comporter exactement 4 chiffres");

// Test 2: Validation OTP
const okCheck = SecurityManager.verifyDeliveryOTP(otp, otp);
assert.strictEqual(okCheck.verified, true);

const failCheck = SecurityManager.verifyDeliveryOTP(otp, "0000");
assert.strictEqual(failCheck.verified, false);
assert(failCheck.error.includes("invalide"));

// Test 3: Signature cryptographique
const sig1 = SecurityManager.computeDataSignature("SECRET", "CMD-101-5000");
const sig2 = SecurityManager.computeDataSignature("SECRET", "CMD-101-5000");
const sig3 = SecurityManager.computeDataSignature("SECRET", "CMD-101-9999");
assert.strictEqual(sig1, sig2, "Deux payloads identiques doivent avoir la même signature");
assert.notStrictEqual(sig1, sig3, "Une altération de données doit changer la signature");

console.log("✅ Tests de sécurité anti-fraude réussis !");
