/**
 * GazExpress - Modèle de données initiales et tarification officielle (Bénin)
 */

export const INITIAL_PRODUCTS = [
  {
    id: "B6_RECHARGE",
    name: "Bouteille 6 kg - Recharge / Échange",
    format: "6kg",
    operation: "recharge",
    description: "Échange standard de bouteille vide contre bouteille pleine (toutes marques confondues selon la réglementation).",
    price: 4950, // Prix officiel client
    depotCost: 4450, // Coût de réapprovisionnement point de vente
    companyMargin: 500, // Marge commerciale entreprise
    image: "assets/b6.png"
  },
  {
    id: "B6_COMPLET",
    name: "Bouteille 6 kg - Achat Complet (Consignation)",
    format: "6kg",
    operation: "complet",
    description: "Bouteille neuve avec charge de gaz 6kg + détendeur + tuyau de sécurité.",
    price: 18500,
    depotCost: 16500,
    companyMargin: 2000,
    image: "assets/b6_full.png"
  },
  {
    id: "B12_RECHARGE",
    name: "Bouteille 12,5 kg - Recharge / Échange",
    format: "12.5kg",
    operation: "recharge",
    description: "Échange standard de bouteille 12,5 kg vide contre une pleine (interchangeabilité autorisée).",
    price: 10300,
    depotCost: 9300,
    companyMargin: 1000,
    image: "assets/b12.png"
  },
  {
    id: "B12_COMPLET",
    name: "Bouteille 12,5 kg - Achat Complet (Consignation)",
    format: "12.5kg",
    operation: "complet",
    description: "Grande bouteille neuve 12,5 kg complète avec gaz + détendeur renforcé + tuyau.",
    price: 32000,
    depotCost: 28500,
    companyMargin: 3500,
    image: "assets/b12_full.png"
  }
];

// Barèmes de livraison configurables (par format)
export const DELIVERY_RATES = {
  "6kg": {
    baseRatePer500m: 500,
    rate1km: 1000,
    extraStepMeters: 500,
    extraStepCost: 500,
    driverPayout: 500 // Paiement fixe garanti au livreur
  },
  "12.5kg": {
    baseRatePer500m: 700,
    rate1km: 1400,
    extraStepMeters: 500,
    extraStepCost: 700,
    driverPayout: 500 // Paiement fixe garanti au livreur
  }
};

// Points de vente / Dépôts agréés géolocalisés (Bénin)
export const INITIAL_DEPOTS = [
  {
    id: "DEPOT_COT_01",
    name: "Dépôt Central Gaz Akpakpa",
    city: "Cotonou",
    zone: "Akpakpa Sacré-Cœur",
    lat: 6.3685,
    lng: 2.4512,
    phone: "+229 97 11 22 33",
    manager: "M. Pedro KPONON",
    stock: {
      "B6_RECHARGE": 45,
      "B6_COMPLET": 12,
      "B12_RECHARGE": 30,
      "B12_COMPLET": 8
    }
  },
  {
    id: "DEPOT_COT_02",
    name: "Station Gaz Haie Vive & Cocotiers",
    city: "Cotonou",
    zone: "Haie Vive",
    lat: 6.3541,
    lng: 2.3986,
    phone: "+229 95 44 55 66",
    manager: "Mme Clarisse S.",
    stock: {
      "B6_RECHARGE": 60,
      "B6_COMPLET": 20,
      "B12_RECHARGE": 40,
      "B12_COMPLET": 15
    }
  },
  {
    id: "DEPOT_COT_03",
    name: "Comptoir Énergie Menontin / Stade",
    city: "Cotonou",
    zone: "Ménontin",
    lat: 6.3812,
    lng: 2.3789,
    phone: "+229 96 77 88 99",
    manager: "M. Hubert TOKPANOU",
    stock: {
      "B6_RECHARGE": 50,
      "B6_COMPLET": 14,
      "B12_RECHARGE": 35,
      "B12_COMPLET": 10
    }
  },
  {
    id: "DEPOT_CAL_01",
    name: "Relais Gaz Calavi Arconville",
    city: "Abomey-Calavi",
    zone: "Arconville / Zogbadjè",
    lat: 6.4468,
    lng: 2.3551,
    phone: "+229 94 12 34 56",
    manager: "M. Rodrigue A.",
    stock: {
      "B6_RECHARGE": 70,
      "B6_COMPLET": 25,
      "B12_RECHARGE": 50,
      "B12_COMPLET": 18
    }
  },
  {
    id: "DEPOT_PN_01",
    name: "Dépôt Gaz Porto-Novo Ouando",
    city: "Porto-Novo",
    zone: "Grand Marché Ouando",
    lat: 6.5056,
    lng: 2.6102,
    phone: "+229 98 22 33 44",
    manager: "M. Félix D.",
    stock: {
      "B6_RECHARGE": 55,
      "B6_COMPLET": 15,
      "B12_RECHARGE": 32,
      "B12_COMPLET": 9
    }
  },
  {
    id: "DEPOT_KET_01",
    name: "18 EITHING SARL - Hub Gaz Kétou",
    city: "Kétou",
    zone: "Centre-Ville / Marché",
    lat: 7.3633,
    lng: 2.5997,
    phone: "+229 44 66 95 87",
    manager: "Direction 18 EITHING",
    stock: {
      "B6_RECHARGE": 80,
      "B6_COMPLET": 30,
      "B12_RECHARGE": 60,
      "B12_COMPLET": 25
    }
  }
];

// Livreurs partenaires enregistrés avec géolocalisation
export const INITIAL_DRIVERS = [
  {
    id: "DRV_01",
    name: "Bio Chabi",
    phone: "+229 97 00 11 22",
    vehicle: "Moto Tricycle Cargo (Plateau)",
    matricule: "AB-4021-RB",
    lat: 6.3670,
    lng: 2.4490,
    isOnline: true,
    totalDeliveries: 42,
    walletBalance: 21000 // 42 * 500f
  },
  {
    id: "DRV_02",
    name: "Sébastien Houngbo",
    phone: "+229 96 11 22 33",
    vehicle: "Moto Boxer avec support 4 bouteilles",
    matricule: "CC-8812-RB",
    lat: 6.3560,
    lng: 2.4010,
    isOnline: true,
    totalDeliveries: 31,
    walletBalance: 15500
  },
  {
    id: "DRV_03",
    name: "Arnaud Dossou",
    phone: "+229 95 22 33 44",
    vehicle: "Moto Haojue Porte-bagages renforcé",
    matricule: "BB-7019-RB",
    lat: 6.3840,
    lng: 2.3750,
    isOnline: true,
    totalDeliveries: 28,
    walletBalance: 14000
  },
  {
    id: "DRV_04",
    name: "Koffi Mensah",
    phone: "+229 94 33 44 55",
    vehicle: "Tricycle Haojin",
    matricule: "AD-1102-RB",
    lat: 6.4450,
    lng: 2.3520,
    isOnline: true,
    totalDeliveries: 50,
    walletBalance: 25000
  }
];

// Opérateurs MoMo et Interconnexions Bancaires disponibles au Bénin
export const MOMO_PROVIDERS = [
  {
    id: "mtn_momo",
    name: "MTN Mobile Money",
    code: "*880#",
    logoText: "MTN MoMo",
    color: "#ffcc00",
    textColor: "#000000",
    prefixPattern: "^(97|96|61|62|66|67|51|52|53|54)"
  },
  {
    id: "moov_money",
    name: "Moov Money",
    code: "*155#",
    logoText: "Moov Money",
    color: "#005baa",
    textColor: "#ffffff",
    prefixPattern: "^(95|94|64|65|68|69|55|56|57)"
  },
  {
    id: "celtiis_cash",
    name: "Celtiis Cash",
    code: "*888#",
    logoText: "Celtiis Cash",
    color: "#e20613",
    textColor: "#ffffff",
    prefixPattern: "^(40|41|42|43|44)"
  }
];

export const CONNECTED_BANKS = [
  { id: "BOA", name: "Bank of Africa (BOA Bénin)", code: "BOABJ" },
  { id: "ECOBANK", name: "Ecobank Bénin", code: "ECOBJ" },
  { id: "UBA", name: "United Bank for Africa (UBA Bénin)", code: "UBABJ" },
  { id: "SGB", name: "Société Générale Bénin", code: "SGBBJ" },
  { id: "NSIA", name: "NSIA Banque Bénin", code: "NSIABJ" }
];
