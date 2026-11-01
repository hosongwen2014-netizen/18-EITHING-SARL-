/**
 * Passerelle d'interconnexion Mobile Money & Virements Bancaires Bénin
 * Supporte :
 * 1. MTN Mobile Money (*880#)
 * 2. Moov Money (*155#)
 * 3. Celtiis Cash (*888#)
 * 4. Banques partenaires (BOA, Ecobank, UBA, SGB, NSIA)
 */

export class PaymentGateway {
  constructor(config = {}) {
    this.merchantId = config.merchantId || "18EITHING-BJ";
    this.environment = config.environment || "sandbox"; // 'sandbox' ou 'production'
    this.bankAccount = config.bankAccount || {
      bankName: "Bank of Africa Bénin (BOA)",
      accountNumber: "BJ061 01001 002345678901 45",
      holder: "18 EITHING SARL"
    };
  }

  /**
   * Valide le numéro de téléphone selon l'opérateur béninois
   */
  validatePhoneNumber(phone, providerId) {
    const cleaned = String(phone).replace(/\s+/g, '').replace(/^\+229/, '');
    if (!/^\d{8}$/.test(cleaned)) {
      return { valid: false, error: "Le numéro doit comporter 8 chiffres (hors indicatif +229)." };
    }

    const prefixes = {
      mtn_momo: ['97', '96', '61', '62', '66', '67', '51', '52', '53', '54'],
      moov_money: ['95', '94', '64', '65', '68', '69', '55', '56', '57'],
      celtiis_cash: ['40', '41', '42', '43', '44']
    };

    const expectedPrefixes = prefixes[providerId];
    if (expectedPrefixes) {
      const match = expectedPrefixes.some(p => cleaned.startsWith(p));
      if (!match) {
        return {
          valid: false,
          error: `Le préfixe du numéro ne correspond pas au réseau sélectionné (${expectedPrefixes.slice(0, 3).join(', ')}...).`
        };
      }
    }

    return { valid: true, cleanedPhone: cleaned };
  }

  /**
   * Simule ou exécute un paiement USSD Push MoMo
   */
  async initiateMomoDebit({ amount, phone, providerId, orderReference }) {
    const check = this.validatePhoneNumber(phone, providerId);
    if (!check.valid) {
      throw new Error(check.error);
    }

    // En environnement de test / sandbox, simulateur USSD
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          status: "SUCCESS",
          transactionId: `TXN-${providerId.toUpperCase()}-${Date.now()}`,
          orderReference,
          amount,
          currency: "XOF",
          creditedTo: this.merchantId,
          timestamp: new Date().toISOString()
        });
      }, 300);
    });
  }

  /**
   * Génère un ordre de virement bancaire pour reverser les encaissements MoMo vers le compte d'entreprise
   */
  generateBankPayoutOrder(orders) {
    const totalCompanyRevenue = orders.reduce((sum, o) => sum + (o.dispatching?.totalCompanyMargin || 0), 0);
    const totalDepotRevenue = orders.reduce((sum, o) => sum + (o.dispatching?.depotAmount || 0), 0);
    const totalDriverPayouts = orders.reduce((sum, o) => sum + (o.dispatching?.driverAmount || 0), 0);
    const totalCollected = orders.reduce((sum, o) => sum + o.totalCustomerToPay, 0);

    return {
      orderId: `VIR-BOA-${Date.now()}`,
      date: new Date().toLocaleDateString('fr-FR'),
      companyAccount: this.bankAccount,
      summary: {
        totalCollected,
        totalCompanyRevenue,
        totalDepotRevenue,
        totalDriverPayouts
      },
      ordersCount: orders.length,
      status: "PRÊT_POUR_EXECUTION"
    };
  }
}
