<img src="images/TruifyLogo.png" width="250" height="81"/>

# truify
<h1>Introduction/Summary</h1>
Truify is an agentic, open source project to help data and AI pratcitioners prepare training data.  Truify provides CLI and web/GUI access to tooling enabling solutions to the following data preparation challenges:
<UL>
<li>Bias (selection, recency, geographical, gender, channel/market)</li>
<li>Compliance (GDPR, EU AI, SOC2, ISO 27001, HIPAA, CCPA)</li>
<li>Privacy (PII, PHI)</li>
<li>Missingness (incomplete, reverse-incremental)</li>
<li>Imbalance (lack of adequate case vs. control in training data)</li>
<li>Misalignment (cannot harmonize)</li>
<li>Inaccessibility (unstructured/semistructured i.e. PDFs and photos)</li>
</UL>
<br>
<center></center><img src="/images/diagram.png"/></center>
<h1>Approach</h1>
Truify addresses each of these problems with known best-practice approaches as follows.
<table>
<tr>
<th>Problem</th>
<th>Approach</th>
</tr>
<tr>
  <td>Bias</td>
  <td>Data balancing through integrating weighting with public standards</td>
</tr>
<tr>
  <td>Compliance</td>
  <td>De-identification, deterministic filtering based on compliance policy, full auditability, including remediation and validation</td>
</tr>
<tr>
  <td>Privacy/Missingness</td>
  <td>Imputation w/”temperature” control (veracity/hallucination), full data synthesis</td>
</tr>
<tr>
  <td>Misalignment</td>
  <td>GenAI-enabled fuzzy matching based on observed records, automated harmonization</td>
</tr>
</table>
<br>
<h1>Benefits</h1>
Through these approaches, practitioners can achieve the following benefits:
<ul>
<li>better accuracy</li>
<li>better recommendations</li>
<li>greater coveragegreater ROI</li>
<li>improved sustainability</li>
<li>lower risk</li>
<li>greater efficiency</li>
<li>greater trust</li>
<li>improved transparency </li>
<li>faster time to value</li>
</ul>

<h1>Getting Started</h1>

To see a sample streamlit application using the truify libraries: <br>
<code>OPENROUTER_API_KEY="your_api_key_here" python -m streamlit run code/main.py</code>

