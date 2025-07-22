# Data Compliance Risk Report

## Data Description
**Shape:** 7043 rows × 21 columns

**Columns:**

- `customerID` (type: int64)
- `gender` (type: object)
- `SeniorCitizen` (type: int64)
- `Partner` (type: object)
- `Dependents` (type: object)
- `tenure` (type: int64)
- `PhoneService` (type: object)
- `MultipleLines` (type: object)
- `InternetService` (type: object)
- `OnlineSecurity` (type: object)
- `OnlineBackup` (type: object)
- `DeviceProtection` (type: object)
- `TechSupport` (type: object)
- `StreamingTV` (type: object)
- `StreamingMovies` (type: object)
- `Contract` (type: object)
- `PaperlessBilling` (type: object)
- `PaymentMethod` (type: object)
- `MonthlyCharges` (type: float64)
- `TotalCharges` (type: object)
- `Churn` (type: int64)

**Sample Data:**

|   customerID | gender   |   SeniorCitizen | Partner   | Dependents   |   tenure | PhoneService   | MultipleLines    | InternetService   | OnlineSecurity   | OnlineBackup   | DeviceProtection   | TechSupport   | StreamingTV   | StreamingMovies   | Contract       | PaperlessBilling   | PaymentMethod             |   MonthlyCharges |   TotalCharges |   Churn |
|-------------:|:---------|----------------:|:----------|:-------------|---------:|:---------------|:-----------------|:------------------|:-----------------|:---------------|:-------------------|:--------------|:--------------|:------------------|:---------------|:-------------------|:--------------------------|-----------------:|---------------:|--------:|
|         4167 | Female   |               0 | Yes       | No           |        1 | No             | No phone service | DSL               | No               | Yes            | No                 | No            | No            | No                | Month-to-month | Yes                | Electronic check          |            29.85 |          29.85 |       0 |
|         2903 | Male     |               0 | No        | No           |       34 | Yes            | No               | DSL               | Yes              | No             | Yes                | No            | No            | No                | One year       | No                 | Mailed check              |            56.95 |        1889.5  |       0 |
|         1541 | Male     |               0 | No        | No           |        2 | Yes            | No               | DSL               | Yes              | Yes            | No                 | No            | No            | No                | Month-to-month | Yes                | Mailed check              |            53.85 |         108.15 |       1 |
|         6110 | Male     |               0 | No        | No           |       45 | No             | No phone service | DSL               | Yes              | No             | Yes                | Yes           | No            | No                | One year       | No                 | Bank transfer (automatic) |            42.3  |        1840.75 |       0 |
|         2180 | Female   |               0 | No        | No           |        2 | Yes            | No               | Fiber optic       | No               | No             | No                 | No            | No            | No                | Month-to-month | Yes                | Electronic check          |            70.7  |         151.65 |       1 |

## Potential Compliance Risks
- **PII Detected:** ['customerID', 'PhoneService', 'MultipleLines']. This data is subject to [GDPR](https://gdpr-info.eu/) Art. 4, [CCPA](https://oag.ca.gov/privacy/ccpa) §1798.140, and [EU AI Act](https://artificialintelligenceact.eu/) Art. 10.
- **Sensitive Attributes Detected:** ['gender', 'SeniorCitizen', 'Dependents']. Special categories under [GDPR](https://gdpr-info.eu/) Art. 9, [EU AI Act](https://artificialintelligenceact.eu/) Art. 10.
- **Automated Decision-Making Risk:** Data may be used for profiling or automated decisions. See [EU AI Act](https://artificialintelligenceact.eu/) Title III, [GDPR](https://gdpr-info.eu/) Art. 22.

## Action Plan
- - Use the de-identification tools in `PII.py` or the deidentify functions in `main.py` to remove or hash PII columns: ['customerID', 'PhoneService', 'MultipleLines'].
- - Review use of sensitive attributes: ['gender', 'SeniorCitizen', 'Dependents']. Limit processing unless necessary and document justification.
- - Ensure transparency and human oversight for any automated decisions. Document logic and provide opt-out where required.

---
*References:* [GDPR]({GDPR_URL}), [CCPA]({CCPA_URL}), [EU AI Act]({EU_AI_ACT_URL})
