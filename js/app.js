/**
 * GazExpress - Application Principale & Moteur Interactif
 */

import { INITIAL_PRODUCTS, INITIAL_DEPOTS, INITIAL_DRIVERS, MOMO_PROVIDERS } from './data.js';
import { calculateDistanceMeters, computeDeliveryFee, computeOrderBreakdown, findNearestDepot, findNearestAvailableDriver, formatDistance } from './calculator.js';

class GazExpressApp {
  constructor() {
    this.products = [...INITIAL_PRODUCTS];
    this.depots = [...INITIAL_DEPOTS];
    this.drivers = [...INITIAL_DRIVERS];
    this.orders = [];

    // État utilisateur par défaut (Cotonou, zone Akpakpa)
    this.clientPos = { lat: 6.3620, lng: 2.4450 };
    this.selectedOperation = 'recharge'; // 'recharge' ou 'complet'
    this.selectedProduct = this.products.find(p => p.id === 'B6_RECHARGE');
    this.selectedMomo = 'mtn_momo';
    this.nearestDepotInfo = null;

    // Cartes Leaflet
    this.clientMap = null;
    this.driverMap = null;
    this.clientMarker = null;
    this.depotMarkersLayer = null;
    this.driverMarkersLayer = null;
    this.deliveryRouteLine = null;

    this.pendingOrder = null;
  }

  init() {
    this.initPreloadedOrders();
    this.setupTabNavigation();
    this.initClientMap();
    this.renderProducts();
    this.updateNearestDepotAndQuote();
    this.setupEventListeners();
    this.renderDepotsTable();
    this.renderDriverDashboard();
    this.renderAdminDashboard();
  }

  initPreloadedOrders() {
    // 3 commandes pré-remplies pour illustrer immédiatement le journal des ventes et le dispatching
    const sampleB6 = this.products.find(p => p.id === 'B6_RECHARGE');
    const sampleB12 = this.products.find(p => p.id === 'B12_RECHARGE');

    const o1 = this.createOrderObject("M. Koffi Mensah", "Quartier Scoa-Gbéto", "97123456", sampleB6, 1200, "mtn_momo", this.depots[0], this.drivers[0], "LIVRÉ", "08:45");
    const o2 = this.createOrderObject("Mme Aïcha Bello", "Cadjehoun derrière l'Aéroport", "95441122", sampleB12, 1800, "moov_money", this.depots[1], this.drivers[1], "LIVRÉ", "10:15");
    const o3 = this.createOrderObject("Dr. Sossa", "Fidjrossè Calvaire", "40112233", sampleB6, 800, "celtiis_cash", this.depots[1], this.drivers[2], "LIVRÉ", "11:30");

    this.orders.push(o1, o2, o3);
  }

  createOrderObject(clientName, address, phone, product, distanceMeters, momoProvider, depot, driver, status = "EN_ROUTE", timeStr = null) {
    const breakdown = computeOrderBreakdown(product, distanceMeters);
    const now = new Date();
    const formattedTime = timeStr || `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    const id = `CMD-${Math.floor(1000 + Math.random() * 9000)}`;

    return {
      id,
      time: formattedTime,
      clientName,
      address,
      phone,
      product,
      distanceMeters,
      formattedDistance: formatDistance(distanceMeters),
      momoProvider,
      depot,
      driver,
      status,
      ...breakdown
    };
  }

  setupTabNavigation() {
    const tabButtons = document.querySelectorAll('.role-tab-btn');
    const views = document.querySelectorAll('.view-panel');

    tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');

        tabButtons.forEach(b => b.classList.remove('active'));
        views.forEach(v => v.classList.remove('active'));

        btn.classList.add('active');
        const targetView = document.getElementById(`view-${targetTab}`);
        if (targetView) targetView.classList.add('active');

        // Réajuster la taille des cartes lors du changement d'onglet
        setTimeout(() => {
          if (targetTab === 'client' && this.clientMap) this.clientMap.invalidateSize();
          if (targetTab === 'livreur' && !this.driverMap) {
            this.initDriverMap();
          } else if (targetTab === 'livreur' && this.driverMap) {
            this.driverMap.invalidateSize();
          }
        }, 150);
      });
    });
  }

  initClientMap() {
    if (typeof L === 'undefined') return;

    this.clientMap = L.map('map-client').setView([this.clientPos.lat, this.clientPos.lng], 14);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap Bénin'
    }).addTo(this.clientMap);

    // Icône Client (Maison bleue)
    const clientIcon = L.divIcon({
      className: 'custom-client-marker',
      html: '<div style="background:#0284c7;color:#fff;border-radius:50%;width:34px;height:34px;display:flex;align-items:center;justify-content:center;border:3px solid #fff;box-shadow:0 3px 8px rgba(0,0,0,0.4);font-size:16px;">🏠</div>',
      iconSize: [34, 34],
      iconAnchor: [17, 17]
    });

    this.clientMarker = L.marker([this.clientPos.lat, this.clientPos.lng], {
      draggable: true,
      icon: clientIcon
    }).addTo(this.clientMap);

    this.clientMarker.bindPopup("<strong>Votre Domicile</strong><br>Glissez ce repère pour ajuster votre adresse.").openPopup();

    this.clientMarker.on('dragend', (e) => {
      const pos = e.target.getLatLng();
      this.clientPos = { lat: pos.lat, lng: pos.lng };
      this.updateNearestDepotAndQuote();
    });

    this.depotMarkersLayer = L.layerGroup().addTo(this.clientMap);
    this.driverMarkersLayer = L.layerGroup().addTo(this.clientMap);

    this.renderDepotsOnMap();
    this.renderDriversOnMap();
  }

  renderDepotsOnMap() {
    if (!this.depotMarkersLayer) return;
    this.depotMarkersLayer.clearLayers();

    const depotIcon = L.divIcon({
      className: 'custom-depot-marker',
      html: '<div style="background:#dc2626;color:#fff;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;border:3px solid #fff;box-shadow:0 3px 8px rgba(0,0,0,0.3);font-size:14px;">🏬</div>',
      iconSize: [32, 32],
      iconAnchor: [16, 16]
    });

    this.depots.forEach(depot => {
      const marker = L.marker([depot.lat, depot.lng], { icon: depotIcon });
      marker.bindPopup(`
        <div style="font-size: 13px;">
          <strong style="color: #dc2626;">${depot.name}</strong><br>
          <em>${depot.city} - ${depot.zone}</em><br>
          📞 ${depot.phone}<br>
          📦 Stock 6kg: <strong>${depot.stock.B6_RECHARGE}</strong> | 12.5kg: <strong>${depot.stock.B12_RECHARGE}</strong>
        </div>
      `);
      this.depotMarkersLayer.addLayer(marker);
    });
  }

  renderDriversOnMap() {
    if (!this.driverMarkersLayer) return;
    this.driverMarkersLayer.clearLayers();

    const driverIcon = L.divIcon({
      className: 'custom-driver-marker',
      html: '<div style="background:#16a34a;color:#fff;border-radius:50%;width:30px;height:30px;display:flex;align-items:center;justify-content:center;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,0.3);font-size:14px;">🛵</div>',
      iconSize: [30, 30],
      iconAnchor: [15, 15]
    });

    this.drivers.filter(d => d.isOnline).forEach(driver => {
      const marker = L.marker([driver.lat, driver.lng], { icon: driverIcon });
      marker.bindPopup(`
        <div style="font-size: 13px;">
          <strong style="color: #16a34a;">Livreur : ${driver.name}</strong><br>
          Véhicule : ${driver.vehicle}<br>
          Statut : 🟢 Disponible
        </div>
      `);
      this.driverMarkersLayer.addLayer(marker);
    });
  }

  initDriverMap() {
    if (typeof L === 'undefined' || this.driverMap) return;

    const activeDriver = this.drivers[0];
    this.driverMap = L.map('map-driver').setView([activeDriver.lat, activeDriver.lng], 14);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap Livreur'
    }).addTo(this.driverMap);

    const drvIcon = L.divIcon({
      className: 'driver-self-marker',
      html: '<div style="background:#16a34a;color:#fff;border-radius:50%;width:36px;height:36px;display:flex;align-items:center;justify-content:center;border:3px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,0.4);font-size:18px;">🛵</div>',
      iconSize: [36, 36],
      iconAnchor: [18, 18]
    });

    L.marker([activeDriver.lat, activeDriver.lng], { icon: drvIcon })
      .addTo(this.driverMap)
      .bindPopup(`<strong>Votre Position Actuelle</strong><br>${activeDriver.name}`)
      .openPopup();
  }

  renderProducts() {
    const container = document.getElementById('products-selection-container');
    if (!container) return;

    const filtered = this.products.filter(p => p.operation === this.selectedOperation);
    if (!filtered.some(p => p.id === this.selectedProduct.id)) {
      this.selectedProduct = filtered[0];
    }

    container.innerHTML = filtered.map(prod => `
      <div class="product-option ${prod.id === this.selectedProduct.id ? 'selected' : ''}" data-product-id="${prod.id}">
        <span class="product-badge">${prod.format === '6kg' ? '6 KG (STANDARD)' : '12,5 KG (GRAND FORMAT)'}</span>
        <div class="product-title">${prod.name}</div>
        <div class="product-price">${prod.price.toLocaleString('fr-FR')} FCFA</div>
        <div class="product-desc">${prod.description}</div>
      </div>
    `).join('');

    container.querySelectorAll('.product-option').forEach(el => {
      el.addEventListener('click', () => {
        const prodId = el.getAttribute('data-product-id');
        this.selectedProduct = this.products.find(p => p.id === prodId);
        this.renderProducts();
        this.updateNearestDepotAndQuote();
      });
    });
  }

  updateNearestDepotAndQuote() {
    this.nearestDepotInfo = findNearestDepot(this.clientPos.lat, this.clientPos.lng, this.depots);
    if (!this.nearestDepotInfo) return;

    const depot = this.nearestDepotInfo.depot;
    const distanceMeters = this.nearestDepotInfo.distanceMeters;

    // Mise à jour de la boîte d'info
    const nameEl = document.getElementById('nearest-depot-name');
    const distEl = document.getElementById('nearest-depot-dist');
    const addrEl = document.getElementById('nearest-depot-address');

    if (nameEl) nameEl.textContent = `📍 ${depot.name}`;
    if (distEl) distEl.textContent = `${this.nearestDepotInfo.formattedDistance} de vous`;
    if (addrEl) addrEl.textContent = `${depot.city} (${depot.zone}) • Gestionnaire : ${depot.manager}`;

    // Calcul du devis
    const breakdown = computeOrderBreakdown(this.selectedProduct, distanceMeters);

    const qGasName = document.getElementById('quote-gas-name');
    const qGasPrice = document.getElementById('quote-gas-price');
    const qDistLabel = document.getElementById('quote-dist-label');
    const qDeliveryFee = document.getElementById('quote-delivery-fee');
    const qTotalPrice = document.getElementById('quote-total-price');
    const btnPayAmount = document.getElementById('btn-pay-amount');
    const rateExpl = document.getElementById('quote-rate-explanation');

    if (qGasName) qGasName.textContent = this.selectedProduct.name;
    if (qGasPrice) qGasPrice.textContent = `${this.selectedProduct.price.toLocaleString('fr-FR')} FCFA`;
    if (qDistLabel) qDistLabel.textContent = `${formatDistance(distanceMeters)}`;
    if (qDeliveryFee) qDeliveryFee.textContent = `${breakdown.deliveryFee.toLocaleString('fr-FR')} FCFA`;
    if (qTotalPrice) qTotalPrice.textContent = `${breakdown.totalCustomerToPay.toLocaleString('fr-FR')} FCFA`;
    if (btnPayAmount) btnPayAmount.textContent = `${breakdown.totalCustomerToPay.toLocaleString('fr-FR')} FCFA`;

    if (rateExpl) {
      if (this.selectedProduct.format === '12.5kg') {
        rateExpl.textContent = "Tarif Grand Format (12,5kg) : 700 F les 500m / 1 400 F le km (+700F par tranche après 1km)";
      } else {
        rateExpl.textContent = "Tarif Standard (6kg) : 500 F les 500m / 1 000 F le km (+500F par tranche après 1km)";
      }
    }

    // Tracer la ligne de livraison sur la carte
    if (this.clientMap) {
      if (this.deliveryRouteLine) {
        this.clientMap.removeLayer(this.deliveryRouteLine);
      }
      this.deliveryRouteLine = L.polyline([
        [this.clientPos.lat, this.clientPos.lng],
        [depot.lat, depot.lng]
      ], {
        color: '#0284c7',
        weight: 4,
        dashArray: '8, 8',
        opacity: 0.8
      }).addTo(this.clientMap);
    }
  }

  setupEventListeners() {
    // Boutons de changement d'opération (Recharge vs Complet)
    const btnRecharge = document.getElementById('btn-op-recharge');
    const btnComplet = document.getElementById('btn-op-complet');

    btnRecharge.addEventListener('click', () => {
      this.selectedOperation = 'recharge';
      btnRecharge.classList.add('active');
      btnComplet.classList.remove('active');
      this.renderProducts();
      this.updateNearestDepotAndQuote();
    });

    btnComplet.addEventListener('click', () => {
      this.selectedOperation = 'complet';
      btnComplet.classList.add('active');
      btnRecharge.classList.remove('active');
      this.renderProducts();
      this.updateNearestDepotAndQuote();
    });

    // Choix MoMo
    const momoOptions = document.querySelectorAll('.momo-opt');
    momoOptions.forEach(opt => {
      opt.addEventListener('click', () => {
        momoOptions.forEach(o => o.classList.remove('active'));
        opt.classList.add('active');
        this.selectedMomo = opt.getAttribute('data-provider');
      });
    });

    // Géolocalisation automatique GPS
    const btnLocate = document.getElementById('btn-refresh-location');
    if (btnLocate) {
      btnLocate.addEventListener('click', () => {
        if ("geolocation" in navigator) {
          btnLocate.textContent = "⏳ Détection GPS...";
          navigator.geolocation.getCurrentPosition(
            (pos) => {
              btnLocate.textContent = "🎯 Me localiser";
              this.clientPos = { lat: pos.coords.latitude, lng: pos.coords.longitude };
              if (this.clientMarker) this.clientMarker.setLatLng([this.clientPos.lat, this.clientPos.lng]);
              if (this.clientMap) this.clientMap.setView([this.clientPos.lat, this.clientPos.lng], 14);
              this.updateNearestDepotAndQuote();
            },
            (err) => {
              btnLocate.textContent = "🎯 Me localiser";
              alert("Impossible d'accéder au GPS. Vous pouvez déplacer le marqueur bleu manuellement.");
            },
            { enableHighAccuracy: true, timeout: 5000 }
          );
        }
      });
    }

    // Bouton de validation de commande
    const btnOrder = document.getElementById('btn-submit-order');
    if (btnOrder) {
      btnOrder.addEventListener('click', () => {
        this.openMomoModal();
      });
    }

    // Modal USSD MoMo
    const btnUssdCancel = document.getElementById('btn-ussd-cancel');
    const btnUssdConfirm = document.getElementById('btn-ussd-confirm');

    if (btnUssdCancel) {
      btnUssdCancel.addEventListener('click', () => {
        document.getElementById('momo-modal').classList.remove('active');
      });
    }

    if (btnUssdConfirm) {
      btnUssdConfirm.addEventListener('click', () => {
        this.processMomoPayment();
      });
    }

    // Formulaire d'inscription livreur
    const formAddDriver = document.getElementById('form-add-driver');
    if (formAddDriver) {
      formAddDriver.addEventListener('submit', (e) => {
        e.preventDefault();
        const newDriver = {
          id: `DRV_${Date.now()}`,
          name: document.getElementById('new-driver-name').value,
          phone: document.getElementById('new-driver-phone').value,
          vehicle: document.getElementById('new-driver-vehicle').value,
          matricule: document.getElementById('new-driver-matricule').value,
          lat: parseFloat(document.getElementById('new-driver-lat').value),
          lng: parseFloat(document.getElementById('new-driver-lng').value),
          isOnline: true,
          totalDeliveries: 0,
          walletBalance: 0
        };

        this.drivers.push(newDriver);
        this.renderDriversOnMap();
        this.renderDriverDashboard();
        formAddDriver.reset();
        alert(`Livreur ${newDriver.name} recruté et inscrit sur la plateforme avec succès !`);
      });
    }

    // Formulaire d'ajout de point de vente
    const formAddDepot = document.getElementById('form-add-depot');
    if (formAddDepot) {
      formAddDepot.addEventListener('submit', (e) => {
        e.preventDefault();
        const newDepot = {
          id: `DEPOT_CUSTOM_${Date.now()}`,
          name: document.getElementById('depot-name').value,
          city: document.getElementById('depot-city').value,
          zone: document.getElementById('depot-zone').value,
          phone: document.getElementById('depot-phone').value,
          manager: "Partenaire Enregistré",
          lat: parseFloat(document.getElementById('depot-lat').value),
          lng: parseFloat(document.getElementById('depot-lng').value),
          stock: { "B6_RECHARGE": 40, "B6_COMPLET": 15, "B12_RECHARGE": 25, "B12_COMPLET": 10 }
        };

        this.depots.push(newDepot);
        this.renderDepotsTable();
        this.renderDepotsOnMap();
        this.updateNearestDepotAndQuote();
        formAddDepot.reset();
        alert(`Point de vente « ${newDepot.name} » ajouté avec succès au réseau national !`);
      });
    }

    // Export Journal
    const btnExportJournal = document.getElementById('btn-export-journal');
    if (btnExportJournal) {
      btnExportJournal.addEventListener('click', () => {
        this.exportSalesToCSV();
      });
    }

    // Export Virement Bancaire
    const btnExportBank = document.getElementById('btn-export-bank');
    if (btnExportBank) {
      btnExportBank.addEventListener('click', () => {
        this.downloadBankTransferOrder();
      });
    }

    // Retrait Livreur
    const btnDriverPayout = document.getElementById('btn-driver-payout');
    if (btnDriverPayout) {
      btnDriverPayout.addEventListener('click', () => {
        const driver = this.drivers[0];
        if (driver.walletBalance <= 0) {
          alert("Votre solde portefeuille est insuffisant.");
          return;
        }
        const amount = driver.walletBalance;
        driver.walletBalance = 0;
        this.renderDriverDashboard();
        alert(`Demande de virement de ${amount.toLocaleString('fr-FR')} FCFA validée vers votre compte MTN MoMo !`);
      });
    }
  }

  openMomoModal() {
    const clientName = document.getElementById('client-name').value || "Client GazExpress";
    const phone = document.getElementById('client-phone').value || "97000000";
    const address = document.getElementById('client-address').value || "Quartier Cotonou";

    if (!this.nearestDepotInfo) return;
    const distanceMeters = this.nearestDepotInfo.distanceMeters;
    const depot = this.nearestDepotInfo.depot;

    // Trouver le livreur disponible le plus proche
    const nearestDriverInfo = findNearestAvailableDriver(this.clientPos.lat, this.clientPos.lng, this.drivers);
    const assignedDriver = nearestDriverInfo ? nearestDriverInfo.driver : this.drivers[0];

    this.pendingOrder = this.createOrderObject(
      clientName,
      address,
      phone,
      this.selectedProduct,
      distanceMeters,
      this.selectedMomo,
      depot,
      assignedDriver
    );

    const promptText = document.getElementById('ussd-prompt-text');
    if (promptText) {
      const momoName = MOMO_PROVIDERS.find(p => p.id === this.selectedMomo)?.name || "MoMo";
      promptText.innerHTML = `
        <strong>${momoName} Bénin</strong><br>
        Débit de <strong>${this.pendingOrder.totalCustomerToPay.toLocaleString('fr-FR')} FCFA</strong><br>
        Bénéficiaire : <strong>18 EITHING SARL (GazExpress)</strong><br>
        Réf: ${this.pendingOrder.id}
      `;
    }

    const pinInput = document.getElementById('ussd-pin-input');
    if (pinInput) pinInput.value = "1234";

    document.getElementById('momo-modal').classList.add('active');
  }

  processMomoPayment() {
    const modal = document.getElementById('momo-modal');
    modal.classList.remove('active');

    if (!this.pendingOrder) return;

    // Validation de la commande
    this.pendingOrder.status = "EN_ROUTE";
    this.orders.unshift(this.pendingOrder);

    // Décrémenter stock du dépôt
    const prodKey = this.pendingOrder.product.id;
    if (this.pendingOrder.depot.stock[prodKey] > 0) {
      this.pendingOrder.depot.stock[prodKey] -= 1;
    }

    // Incrémenter portefeuille du livreur (500 F fixe)
    this.pendingOrder.driver.walletBalance += 500;
    this.pendingOrder.driver.totalDeliveries += 1;

    // Activer l'affichage du suivi en temps réel côté client
    const tracker = document.getElementById('live-order-tracker');
    if (tracker) {
      tracker.style.display = 'block';
      document.getElementById('tracker-order-id').textContent = `#${this.pendingOrder.id}`;
      document.getElementById('tracker-status-text').textContent = `Livreur assigné : ${this.pendingOrder.driver.name} (${this.pendingOrder.driver.vehicle})`;
      document.getElementById('tracker-depot-name').textContent = this.pendingOrder.depot.name;
      document.getElementById('tracker-distance').textContent = this.pendingOrder.formattedDistance;
    }

    // Mettre à jour tous les tableaux de bord
    this.renderDepotsTable();
    this.renderDriverDashboard();
    this.renderAdminDashboard();

    alert(`🎉 Paiement MoMo réussi ! Votre commande #${this.pendingOrder.id} est validée. Le livreur ${this.pendingOrder.driver.name} se rend au point de vente pour récupérer votre gaz.`);
    this.pendingOrder = null;
  }

  renderDepotsTable() {
    const tbody = document.getElementById('table-depots-body');
    const badge = document.getElementById('depots-count-badge');
    if (!tbody) return;

    if (badge) badge.textContent = `${this.depots.length} dépôts recensés`;

    tbody.innerHTML = this.depots.map(depot => `
      <tr>
        <td>
          <strong>${depot.name}</strong><br>
          <span style="font-size:0.75rem; color:#64748b;">${depot.id}</span>
        </td>
        <td>${depot.city} (${depot.zone})</td>
        <td><code>${depot.lat.toFixed(4)}, ${depot.lng.toFixed(4)}</code></td>
        <td>
          <span style="color:#0284c7; font-weight:700;">${depot.stock.B6_RECHARGE}</span> rech. /
          <span>${depot.stock.B6_COMPLET}</span> comp.
        </td>
        <td>
          <span style="color:#0284c7; font-weight:700;">${depot.stock.B12_RECHARGE}</span> rech. /
          <span>${depot.stock.B12_COMPLET}</span> comp.
        </td>
        <td>${depot.phone}</td>
        <td>
          <button style="padding:4px 8px; font-size:0.75rem; background:#0284c7; color:#fff; border:none; border-radius:4px; cursor:pointer;" onclick="window.locateDepot('${depot.id}')">Voir</button>
        </td>
      </tr>
    `).join('');
  }

  renderDriverDashboard() {
    const activeDriver = this.drivers[0];
    const walletEl = document.getElementById('driver-wallet-val');
    const tripsEl = document.getElementById('driver-trips-count');
    const nameEl = document.getElementById('driver-active-name');
    const listEl = document.getElementById('driver-orders-list');

    if (walletEl) walletEl.textContent = `${activeDriver.walletBalance.toLocaleString('fr-FR')} FCFA`;
    if (tripsEl) tripsEl.textContent = activeDriver.totalDeliveries;
    if (nameEl) nameEl.textContent = activeDriver.name;

    if (listEl) {
      const driverOrders = this.orders.filter(o => o.driver.id === activeDriver.id);
      if (driverOrders.length === 0) {
        listEl.innerHTML = `<p style="color:#64748b; font-size:0.85rem; padding:12px;">Aucune course en attente.</p>`;
      } else {
        listEl.innerHTML = driverOrders.map(order => `
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="color:#0f172a;">${order.id} • ${order.clientName}</strong>
              <span class="tag-status ${order.status === 'LIVRÉ' ? 'completed' : 'in_transit'}">${order.status}</span>
            </div>
            <div style="font-size:0.82rem; color:#475569; margin:6px 0;">
              📍 Dépôt : <strong>${order.depot.name}</strong> ➔ Destination : <strong>${order.address}</strong> (${order.formattedDistance})<br>
              📦 Bouteille : ${order.product.name}<br>
              💰 Votre gain fixe : <strong style="color:#16a34a;">+500 FCFA</strong> (Règlement MoMo garanti)
            </div>
            ${order.status !== 'LIVRÉ' ? `
              <button style="background:#16a34a; color:#fff; border:none; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700; cursor:pointer;" onclick="window.markOrderDelivered('${order.id}')">
                ✔ Confirmer la livraison au client
              </button>
            ` : '<span style="font-size:0.75rem; color:#16a34a;">✔ Course terminée & rétribution créditée</span>'}
          </div>
        `).join('');
      }
    }
  }

  renderAdminDashboard() {
    // Calculs de synthèse des KPIs
    let totalCA = 0;
    let totalDepots = 0;
    let totalDrivers = 0;
    let totalCompany = 0;

    this.orders.forEach(o => {
      totalCA += o.totalCustomerToPay;
      totalDepots += o.dispatching.depotAmount;
      totalDrivers += o.dispatching.driverAmount;
      totalCompany += o.dispatching.totalCompanyMargin;
    });

    const caEl = document.getElementById('kpi-total-ca');
    const depEl = document.getElementById('kpi-total-depots');
    const drvEl = document.getElementById('kpi-total-drivers');
    const compEl = document.getElementById('kpi-total-company');

    if (caEl) caEl.textContent = `${totalCA.toLocaleString('fr-FR')} FCFA`;
    if (depEl) depEl.textContent = `${totalDepots.toLocaleString('fr-FR')} FCFA`;
    if (drvEl) drvEl.textContent = `${totalDrivers.toLocaleString('fr-FR')} FCFA`;
    if (compEl) compEl.textContent = `${totalCompany.toLocaleString('fr-FR')} FCFA`;

    // Remplissage du journal des ventes
    const tbody = document.getElementById('table-sales-body');
    if (tbody) {
      tbody.innerHTML = this.orders.map(order => `
        <tr>
          <td>
            <strong>${order.time}</strong><br>
            <span style="font-size:0.72rem; color:#64748b;">${order.id}</span>
          </td>
          <td>
            <strong>${order.clientName}</strong><br>
            <span style="font-size:0.72rem; color:#64748b;">${order.address}</span>
          </td>
          <td>
            <span class="product-badge" style="background:#0284c7;">${order.product.format}</span> ${order.product.operation === 'recharge' ? 'Recharge' : 'Complet'}
          </td>
          <td>${order.formattedDistance}</td>
          <td><strong style="color:#0284c7;">${order.totalCustomerToPay.toLocaleString('fr-FR')} F</strong></td>
          <td>${order.dispatching.depotAmount.toLocaleString('fr-FR')} F</td>
          <td><strong style="color:#8b5cf6;">${order.dispatching.driverAmount.toLocaleString('fr-FR')} F</strong></td>
          <td><strong style="color:#16a34a;">${order.dispatching.totalCompanyMargin.toLocaleString('fr-FR')} F</strong></td>
          <td>
            <span class="tag-status ${order.status === 'LIVRÉ' ? 'completed' : 'in_transit'}">${order.status}</span>
          </td>
        </tr>
      `).join('');
    }
  }

  downloadBankTransferOrder() {
    let totalCA = 0;
    let totalDepots = 0;
    let totalDrivers = 0;
    let totalCompany = 0;

    this.orders.forEach(o => {
      totalCA += o.totalCustomerToPay;
      totalDepots += o.dispatching.depotAmount;
      totalDrivers += o.dispatching.driverAmount;
      totalCompany += o.dispatching.totalCompanyMargin;
    });

    const dateStr = new Date().toLocaleDateString('fr-FR');
    const orderDoc = `========================================================================
ORDRE DE VIREMENT BANCAIRE AUTOMATIQUE & REVERSEMENT JOURNALIER
RÉPUBLIQUE DU BÉNIN - INTERCONNEXION MOMO & SYSTÈME BANCAIRE
========================================================================
Date d'émission : ${dateStr}
Émetteur       : Passerelle Nationale MoMo GazExpress (MTN, Moov, Celtiis)
Bénéficiaire   : 18 EITHING SARL
Compte Bancaire : Bank of Africa Bénin (BOA)
RIB / IBAN      : BJ061 01001 002345678901 45
Domaine Officiel: contact@18eithing.bj | Kétou, Bénin

------------------------------------------------------------------------
RÉSUMÉ DU DISPATCHING JOURNALIER DES COMPTES
------------------------------------------------------------------------
Nombre de transactions MoMo traitées   : ${this.orders.length}
Total brut collecté via Mobile Money    : ${totalCA.toLocaleString('fr-FR')} FCFA
- Part à reverser aux Dépôts Partenaires : ${totalDepots.toLocaleString('fr-FR')} FCFA
- Part reversée aux Livreurs (500F fixe) : ${totalDrivers.toLocaleString('fr-FR')} FCFA
- MARGE NETTE ENCAISSÉE PAR L'ENTREPRISE : ${totalCompany.toLocaleString('fr-FR')} FCFA

------------------------------------------------------------------------
VIREMENT BANCAIRE CONFIRMÉ VERS LE COMPTE 18 EITHING SARL : ${totalCompany.toLocaleString('fr-FR')} FCFA
========================================================================`;

    const blob = new Blob([orderDoc], { type: 'text/plain;charset=utf-8' });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `ordre_virement_boa_18eithing_${new Date().toISOString().slice(0, 10)}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  exportSalesToCSV() {
    const headers = ["ID", "Heure", "Client", "Adresse", "Produit", "Distance", "Total_Paye_MoMo", "Part_Depot", "Part_Livreur", "Marge_Entreprise", "Statut"];
    const rows = this.orders.map(o => [
      o.id,
      o.time,
      `"${o.clientName}"`,
      `"${o.address}"`,
      `"${o.product.name}"`,
      o.distanceMeters,
      o.totalCustomerToPay,
      o.dispatching.depotAmount,
      o.dispatching.driverAmount,
      o.dispatching.totalCompanyMargin,
      o.status
    ]);

    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `gazexpress_point_journalier_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

// Initialisation globale
window.addEventListener('DOMContentLoaded', () => {
  window.app = new GazExpressApp();
  window.app.init();

  // Méthodes globales pour les interactions boutons
  window.markOrderDelivered = (orderId) => {
    const order = window.app.orders.find(o => o.id === orderId);
    if (order) {
      order.status = "LIVRÉ";
      window.app.renderDriverDashboard();
      window.app.renderAdminDashboard();
      alert(`Course #${orderId} marquée comme livrée avec succès !`);
    }
  };

  window.locateDepot = (depotId) => {
    const depot = window.app.depots.find(d => d.id === depotId);
    if (depot && window.app.clientMap) {
      document.getElementById('tab-btn-client').click();
      window.app.clientMap.setView([depot.lat, depot.lng], 16);
    }
  };
});
