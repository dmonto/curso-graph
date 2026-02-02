def detectar_features_disponibles(sku_part_number):
    """
    Basado en SKU, determina qué features están disponibles
    
    VENTAJA: Saber qué mostrar al usuario
    """
    
    print("=" * 70)
    print("DETECTOR DE FEATURES DISPONIBLES")
    print("=" * 70)
    
    sku = sku_part_number.upper()
    
    # Base para todos
    features = {
        "Teams": True,
        "Exchange": False,  # E1 solo web
        "SharePoint": True,
        "OneDrive": True,
        "Planner_Básico": True,
        "Planner_Premium": False,  # Solo E5
        "Power_BI": False,
        "Advanced_Security": False,
        "Advanced_Compliance": False
    }
    
    # E1 (Básico)
    if sku.startswith("MICROSOFT365_BUSINESS_BASIC") or sku == "SPE_E1":
        features.update({
            "Exchange": False,  # Solo web
            "Planner_Básico": True
        })
        tier = "🟢 E1 - BÁSICO"
    
    # E3 (Estándar)
    elif sku == "SPE_E3" or "E3" in sku:
        features.update({
            "Exchange": True,  # Full
            "Planner_Básico": True,
            "Power_BI": False
        })
        tier = "🟡 E3 - ESTÁNDAR"
    
    # E5 (Premium)
    elif sku == "SPE_E5" or "E5" in sku:
        features.update({
            "Exchange": True,
            "Planner_Básico": True,
            "Planner_Premium": True,  # ← Premium
            "Power_BI": True,
            "Advanced_Security": True,
            "Advanced_Compliance": True
        })
        tier = "🔴 E5 - PREMIUM"
    
    # F (Frontline)
    elif "F" in sku:
        features.update({
            "Exchange": False,
            "Planner_Básico": True
        })
        tier = "🟠 F - FRONTLINE"
    
    # Mostrar
    print(f"\nSKU: {sku}")
    print(f"TIER: {tier}\n")
    print("Features disponibles:")
    
    for feature, disponible in features.items():
        estado = "✅" if disponible else "❌"
        print(f"  {estado} {feature.replace('_', ' ')}")
    
    return {
        "sku": sku,
        "tier": tier,
        "features": features
    }

# EJEMPLOS:

print("\n1️⃣  E1 (Básico):\n")
detectar_features_disponibles("SPE_E1")

print("\n" + "=" * 70)
print("\n2️⃣  E3 (Estándar):\n")
detectar_features_disponibles("SPE_E3")

print("\n" + "=" * 70)
print("\n3️⃣  E5 (Premium):\n")
detectar_features_disponibles("SPE_E5")