import { useContext } from "react";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import AuthContext from "../../context/AuthContext.jsx";

const plans = [
  {
    id: "regular",
    name: "Regular",
    price: 0,
    features: ["Basic shipping", "Shipping weight limit up to 5 kg"],
  },
  {
    id: "premium",
    name: "Premium",
    price: 50,
    features: [
      "Shipping weight limit up to 20 kg",
      "Real-time shipment tracking",
      "Unlimited shipments",
      "Phone and email customer support",
      "Discounts on bulk shipments",
    ],
  },
  {
    id: "business",
    name: "Business",
    price: 150,
    features: [
      "Shipping weight limit up to 50 kg",
      "Advanced tracking with instant alerts",
      "Unlimited priority shipments",
      "24/7 support via phone, email, and chat",
      "Detailed reports and monthly shipment analytics",
      "Multiple user accounts per company",
    ],
  },
];

export default function Payment() {
  const { user, api } = useContext(AuthContext);

  const handleUpgrade = async (planId) => {
    try {
      await api.post("/account/upgrade/", { plan_id: planId });
      alert("Plan upgraded successfully!");
      window.location.href = "/dashboard";
    } catch (error) {
      console.error("Upgrade failed:", error.response?.data || error.message);
      alert("Plan upgrade failed.");
    }
  };

  return (
    <PayPalScriptProvider options={{ "client-id": "AeR1Lb5gdCtQfg_6YW3fzK57h4xK-aOlLLaVK4AYScutG3zZ82xkMw0ZC06HHezF-WaSdEYl454IPhBg" }}>
      <div style={{ maxWidth: 1200, margin: "auto", padding: "40px 20px", fontFamily: "sans-serif" }}>
        <h1 style={{ textAlign: "center", color: "#009689", marginBottom: 40, fontSize: 30, fontWeight: "bold" }}>
          Upgrade Your Shipping Plan
        </h1>
        <div style={{ display: "flex", gap: 30, justifyContent: "center", flexWrap: "wrap" }}>
          {plans.map((plan) => {
            const currentPlanName = user?.current_plan?.name?.toLowerCase();
            const isCurrent = currentPlanName === plan.id.toLowerCase();

            return (
              <div
                key={plan.id}
                style={{
                  border: isCurrent ? "2px solid #009689" : "1px solid #ccc",
                  borderRadius: 12,
                  padding: 30,
                  width: 350,
                  backgroundColor: isCurrent ? "#e0f7f5" : "#fff",
                  boxShadow: "0 4px 10px rgba(0,0,0,0.08)",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                  height: 520,
                }}
              >
                <div>
                  <h3 style={{ color: "#009689", fontSize: 24, marginBottom: 10 }}>{plan.name}</h3>
                  <p style={{ fontSize: 18, fontWeight: "bold" }}>${plan.price}</p>
                  <ul style={{ paddingLeft: 20, marginBottom: 20 }}>
                    {plan.features.map((feature, i) => (
                      <li key={i} style={{ marginBottom: 8 }}>{feature}</li>
                    ))}
                  </ul>
                </div>
                <div style={{ marginTop: "auto" }}>
                  {isCurrent ? (
                    <button
                      style={{
                        padding: "10px 20px",
                        backgroundColor: "#ccc",
                        border: "none",
                        borderRadius: 6,
                        color: "#333",
                        cursor: "not-allowed",
                        width: "100%",
                      }}
                      disabled
                    >
                      Current Plan
                    </button>
                  ) : plan.price === 0 ? (
                    <button
                      style={{
                        padding: "10px 20px",
                        backgroundColor: "#009689",
                        border: "none",
                        borderRadius: 6,
                        color: "#fff",
                        cursor: "pointer",
                        width: "100%",
                      }}
                      onClick={() => handleUpgrade(plan.id)}
                    >
                      Choose Free Plan
                    </button>
                  ) : (
                    <PayPalButtons
                      style={{ layout: "vertical", label: "pay", color: "gold" }}
                      createOrder={(data, actions) => {
                        return actions.order.create({
                          purchase_units: [
                            {
                              amount: {
                                value: plan.price.toString(),
                              },
                            },
                          ],
                        });
                      }}
                      onApprove={async (data, actions) => {
                        await actions.order.capture();
                        await handleUpgrade(plan.id);
                      }}
                    />
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </PayPalScriptProvider>
  );
}