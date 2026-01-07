. Problem (Business First)

Global inflation and commodity volatility create cost uncertainty for manufacturers and supply-chain teams. Reactive analysis leads to delayed decisions and margin loss.

2. Analytics Solution (Not Tools)

This project builds a real-time supply-chain risk analytics system that detects volatility-driven price risk using time-series SQL analytics and exposes a trusted Golden View for decision-making.

3. Data Architecture (Signal of Maturity)

Implemented a Medallion Architecture (Raw → Clean → Golden) in PostgreSQL to ensure data quality, idempotency, and explainability.

4. Core Analytics (THIS IS YOUR WEAPON)

Rolling averages to capture trend

Rolling volatility to quantify instability

Risk categorization combining volatility + direction

No ML mentioned yet.

5. Forecasting (Support Feature)

A short-term price forecast is used to anticipate near-term risk escalation and support proactive decisions.