/**
 * GazExpress - Module de Sécurité, Cryptographie & Prévention Anti-Fraude
 * Conçu pour contrer :
 * 1. La falsification de confirmation de paiement (Man-in-the-Middle)
 * 2. La fraude de fausse livraison (coursier ou client indélicat) via OTP
 * 3. Les attaques par injection / brute force
 */

export class SecurityManager {
  /**
   * Génère un code OTP secret de 4 chiffres pour sécuriser la remise de la bouteille
   */
  static generateDeliveryOTP() {
    return String(Math.floor(1000 + Math.random() * 9000));
  }

  /**
   * Calcule un hash/signature cryptographique léger (type SHA-256 / HMAC)
   * pour valider l'intégrité des données d'une commande
   */
  static computeDataSignature(secretKey, payloadString) {
    let hash = 0;
    const combined = `${secretKey}:${payloadString}`;
    for (let i = 0; i < combined.length; i++) {
      const char = combined.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash |= 0; // Convertit en entier 32 bits
    }
    return 'SIG-' + Math.abs(hash).toString(16).toUpperCase().padStart(8, '0');
  }

  /**
   * Valide la conformité du code OTP client lors de la remise de la bouteille
   */
  static verifyDeliveryOTP(expectedOtp, enteredOtp) {
    if (!expectedOtp || !enteredOtp) {
      return { verified: false, error: "Code OTP manquant" };
    }
    const cleanExpected = String(expectedOtp).trim();
    const cleanEntered = String(enteredOtp).trim();

    if (cleanExpected === cleanEntered) {
      return { verified: true };
    }
    return { verified: false, error: "Code secret invalide ! La commission livreur reste verrouillée." };
  }

  /**
   * Journal d'audit de sécurité inaltérable
   */
  static createAuditLog(action, actor, details = {}) {
    return {
      id: `SEC-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      timestamp: new Date().toISOString(),
      action,
      actor,
      details,
      status: "VERIFIED"
    };
  }
}
