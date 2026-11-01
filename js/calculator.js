/**
 * GazExpress - Moteur de Calcul des Tarifs, Distances et Marges
 */

import { DELIVERY_RATES } from './data.js';

/**
 * Calcule la distance orthodromique (en mètres) entre deux coordonnées GPS
 * Formule de Haversine
 */
export function calculateDistanceMeters(lat1, lon1, lat2, lon2) {
  const R = 6371e3; // Rayon moyen de la terre en mètres
  const phi1 = (lat1 * Math.PI) / 180;
  const phi2 = (lat2 * Math.PI) / 180;
  const deltaPhi = ((lat2 - lat1) * Math.PI) / 180;
  const deltaLambda = ((lon2 - lon1) * Math.PI) / 180;

  const a =
    Math.sin(deltaPhi / 2) * Math.sin(deltaPhi / 2) +
    Math.cos(phi1) * Math.cos(phi2) *
    Math.sin(deltaLambda / 2) * Math.sin(deltaLambda / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return Math.round(R * c);
}

/**
 * Formate une distance en mètres ou kilomètres lisible
 */
export function formatDistance(meters) {
  if (meters < 1000) {
    return `${meters} m`;
  }
  return `${(meters / 1000).toFixed(2)} km`;
}

/**
 * Règle de tarification de la livraison selon les spécifications :
 * - 6kg : 500 F les 500m, 1000 F pour 1 km (1000m), puis +500 F par tranche entamée de 500m au-delà.
 * - 12.5kg : 700 F les 500m, 1400 F pour 1 km (1000m), puis +700 F par tranche entamée de 500m au-delà.
 * - La rétribution fixe du livreur est de 500 F.
 * - La marge de livraison pour l'entreprise = tarif_livraison - 500 F.
 */
export function computeDeliveryFee(distanceMeters, format = "6kg", customRates = DELIVERY_RATES) {
  const safeMeters = Math.max(1, Math.round(distanceMeters));
  const rateConfig = customRates[format] || customRates["6kg"];

  const stepCost = (format === "12.5kg") ? 700 : 500;
  const driverPayout = 500;

  let deliveryFee = 0;

  if (safeMeters <= 500) {
    deliveryFee = stepCost;
  } else if (safeMeters <= 1000) {
    deliveryFee = stepCost * 2; // 1000 F pour 6kg, 1400 F pour 12.5kg
  } else {
    // Au-delà de 1000m : base de 1000m + tranches de 500m entamées
    const extraMeters = safeMeters - 1000;
    const additionalSteps = Math.ceil(extraMeters / 500);
    deliveryFee = (stepCost * 2) + (additionalSteps * stepCost);
  }

  const companyDeliveryMargin = Math.max(0, deliveryFee - driverPayout);

  return {
    distanceMeters: safeMeters,
    formattedDistance: formatDistance(safeMeters),
    format,
    deliveryFee,
    driverPayout,
    companyDeliveryMargin
  };
}

/**
 * Trouve le point de vente le plus proche d'un point client (lat, lng)
 */
export function findNearestDepot(clientLat, clientLng, depots) {
  if (!depots || depots.length === 0) return null;

  let nearest = null;
  let minDistance = Infinity;

  for (const depot of depots) {
    const dist = calculateDistanceMeters(clientLat, clientLng, depot.lat, depot.lng);
    if (dist < minDistance) {
      minDistance = dist;
      nearest = {
        depot,
        distanceMeters: dist,
        formattedDistance: formatDistance(dist)
      };
    }
  }

  return nearest;
}

/**
 * Trouve le livreur disponible le plus proche du client ou du dépôt
 */
export function findNearestAvailableDriver(targetLat, targetLng, drivers) {
  const activeDrivers = (drivers || []).filter(d => d.isOnline !== false);
  if (activeDrivers.length === 0) return null;

  let nearest = null;
  let minDistance = Infinity;

  for (const driver of activeDrivers) {
    const dist = calculateDistanceMeters(targetLat, targetLng, driver.lat, driver.lng);
    if (dist < minDistance) {
      minDistance = dist;
      nearest = {
        driver,
        distanceMeters: dist,
        formattedDistance: formatDistance(dist)
      };
    }
  }

  return nearest;
}

/**
 * Calcul complet de la commande et du dispatching des montants
 */
export function computeOrderBreakdown(product, distanceMeters, customRates = DELIVERY_RATES) {
  const delivery = computeDeliveryFee(distanceMeters, product.format, customRates);
  const gasPrice = product.price;
  const totalCustomerToPay = gasPrice + delivery.deliveryFee;

  const depotAmount = product.depotCost;
  const companyGasMargin = product.companyMargin || (product.price - product.depotCost);
  const driverAmount = delivery.driverPayout; // 500 F
  const companyDeliveryMargin = delivery.companyDeliveryMargin;
  const totalCompanyMargin = companyGasMargin + companyDeliveryMargin;

  return {
    product,
    gasPrice,
    deliveryFee: delivery.deliveryFee,
    totalCustomerToPay,
    dispatching: {
      depotAmount,
      driverAmount,
      companyGasMargin,
      companyDeliveryMargin,
      totalCompanyMargin
    },
    deliveryDetails: delivery
  };
}
