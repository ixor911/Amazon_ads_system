# AI Marketing Agent System — README

## Project Summary

This project is an MVP prototype of an AI Marketing Agent system for Amazon Ads campaign optimization.

The system was designed for the Smartwash launch case study. Its main goal is to support marketing teams by analyzing campaign, product, and keyword performance data, generating optimization recommendations, validating actions, and preparing them for human review.

The current prototype is implemented in n8n and works in recommendation-only mode. It does not execute live Amazon Ads changes yet.


## Project Structure

1. Context Layer

   1.1 DataExtractor

   1.2 MetricsEngine

   1.3 EntityBuilder

   1.4 DecisionPolicyEngine

   1.5 ContextAssembler


2. AI Agents Layer

   2.1 MarketingOptimizationAgent

   2.2 Execution Agent


3. Main Orchestrator



## 1. Context Layer

### 1.1 DataExtractor

DataExtractor retrieves raw Amazon Ads performance data from the internal n8n database.

Input:

{
  "mode": "campaign",
  "conditions": {
    "campaign_id": "CAMP_A"
  }
}

The workflow can work with different analysis modes:

- campaign
- product
- keyword

Depending on the selected mode and conditions, it filters data by fields such as campaign_id, asin, keyword_target, and date_from if provided.

Output:

Returns a list of raw Amazon Ads performance records.

Example output item:

{
  "date": "2026-04-03T22:00:00.000Z",
  "market": "DE",
  "campaign_id": "CAMP_A",
  "campaign_name": "Smartwash Launch - Broad Discovery",
  "asin": "SWASH_001",
  "product_name": "Smartwash Universal Detergent",
  "keyword_target": "laundry detergent",
  "impressions": 13270,
  "clicks": 72,
  "spend": 82.52,
  "orders": 3,
  "sales": 50.55,
  "bid": 1.32,
  "daily_budget": 500,
  "id": 1,
  "createdAt": "2026-05-04T14:30:14.308Z",
  "updatedAt": "2026-05-04T14:30:14.308Z"
}


### 1.2 MetricsEngine

MetricsEngine receives raw performance records and calculates aggregated advertising metrics.

Input:

A list of raw data records from DataExtractor.

Before calculating final KPIs, the workflow creates a base summary:

{
  "sum_impressions": 17918,
  "sum_clicks": 71,
  "sum_orders": 4,
  "sum_spend": 95.64,
  "sum_sales": 61.35,
  "average_bid": 1.45
}

Then it calculates additional metrics:

- CTR = clicks / impressions
- CVR = orders / clicks
- CPC = spend / clicks
- ROAS = sales / spend
- ACoS = spend / sales

Output:

{
  "summary": {
    "sum_impressions": 17918,
    "sum_clicks": 71,
    "sum_orders": 4,
    "sum_spend": 95.64,
    "sum_sales": 61.35,
    "average_bid": 1.45,
    "ctr": 0.00396,
    "cvr": 0.05634,
    "cpc": 1.35,
    "roas": 0.64,
    "acos": 1.56
  }
}


### 1.3 EntityBuilder

EntityBuilder creates a structured entity description for the selected analysis object.

Input:

{
  "mode": "campaign",
  "conditions": {
    "campaign_id": "CAMP_A",
    "date_from": "2026-04-20"
  }
}

The workflow supports entity building for:

- campaign
- product
- keyword

For campaign mode, it collects campaign metadata, related products, related keywords, market, budget, and date range.

Output:

{
  "entity": {
    "type": "campaign",
    "id": "CAMP_A",
    "name": "Smartwash Launch - Broad Discovery",
    "market": "DE",
    "daily_budget": 500,
    "products": [
      "SWASH_001",
      "SWASH_002",
      "SWASH_003"
    ],
    "keywords": [
      "cheap detergent",
      "fresh laundry scent",
      "laundry detergent",
      "washing liquid"
    ],
    "days_amount": 13,
    "date_range": {
      "min_date": "2026-04-20",
      "max_date": "2026-05-02"
    }
  }
}

### 1.4 DecisionPolicyEngine

DecisionPolicyEngine defines which business actions are allowed for the selected analysis mode and which guardrails must be applied.

Input:

{
  "mode": "campaign"
}

The workflow supports different policy configurations for:

- campaign
- product
- keyword

For campaign mode, it allows campaign-level optimization actions such as bid changes, budget changes, campaign pause, product analysis, and keyword analysis.

Output:

{
  "policy": {
    "business_actions": [
      "increase_bid",
      "decrease_bid",
      "increase_budget",
      "decrease_budget",
      "pause_campaign",
      "analyze_products",
      "analyze_keywords",
      "keep_current_settings"
    ],
    "guardrails": {
      "human_approval_required": true,
      "do_not_execute_live_changes": true,
      "max_bid_change_pct": 20,
      "max_budget_change_pct": 25,
      "require_reason_for_each_action": true
    }
  }
}

### 1.5 ContextAssembler

ContextAssembler builds the complete decision context required for the AI agent.

It receives the original user request and executes the context-related modules:

- DataExtractor
- MetricsEngine
- EntityBuilder
- DecisionPolicyEngine

Input:

{
  "request": {
    "mode": "campaign",
    "conditions": {
      "campaign_id": "CAMP_A",
      "date_from": "2026-04-20"
    },
    "objective": {
      "primary": "increase_efficiency",
      "secondary": [
        "reduce_acos",
        "improve_roas"
      ]
    },
    "additions": "",
    "detail_level": "detailed",
    "automation_level": "recommendation_only"
  }
}

The workflow combines the original request with the generated policy, entity description, and performance summary.

Output:

{
  "request": {
    "mode": "campaign",
    "conditions": {
      "campaign_id": "CAMP_A",
      "date_from": "2026-04-20"
    },
    "objective": {
      "primary": "increase_efficiency",
      "secondary": [
        "reduce_acos",
        "improve_roas"
      ]
    },
    "additions": "",
    "detail_level": "detailed",
    "automation_level": "recommendation_only"
  },
  "policy": {
    "business_actions": [
      "increase_bid",
      "decrease_bid",
      "increase_budget",
      "decrease_budget",
      "pause_campaign",
      "analyze_products",
      "analyze_keywords",
      "keep_current_settings"
    ],
    "guardrails": {
      "human_approval_required": true,
      "do_not_execute_live_changes": true,
      "max_bid_change_pct": 20,
      "max_budget_change_pct": 25,
      "require_reason_for_each_action": true
    }
  },
  "entity": {
    "type": "campaign",
    "id": "CAMP_A",
    "name": "Smartwash Launch - Broad Discovery",
    "market": "DE",
    "daily_budget": 500,
    "products": [
      "SWASH_001",
      "SWASH_002",
      "SWASH_003"
    ],
    "keywords": [
      "cheap detergent",
      "fresh laundry scent",
      "laundry detergent",
      "washing liquid"
    ],
    "days_amount": 13,
    "date_range": {
      "min_date": "2026-04-20",
      "max_date": "2026-05-02"
    }
  },
  "summary": {
    "sum_impressions": 1550634,
    "sum_clicks": 5537,
    "sum_orders": 205,
    "sum_spend": 5327.55,
    "sum_sales": 3723.8,
    "average_bid": 1.13,
    "ctr": 0.00357,
    "cvr": 0.03702,
    "cpc": 0.96,
    "roas": 0.7,
    "acos": 1.43
  }
}



## 2. AI Agents Layer

### 2.1 MarketingOptimizationAgent

MarketingOptimizationAgent is the main AI decision-making module.

It receives the prepared decision context from ContextAssembler and generates structured Amazon Ads optimization recommendations.

### Input:

{
  "request": {...},
  "policy": {...},
  "entity": {...},
  "summary": {...}
}

AI model:
- GPT-5-mini

### System Message:

You are a Marketing Optimization Agent for Amazon Ads.

Your task is to analyze the provided decision_context and return structured recommendations.

The decision_context contains:
- request: user intent, selected mode, filters, objective, detail level, and automation level
- policy: allowed business actions and guardrails
- entity: the campaign/product/keyword being analyzed
- summary: aggregated performance metrics

Important rules:
1. Use ONLY the data provided in decision_context.
2. Do NOT invent missing data.
3. Do NOT claim that metrics are missing if they are present in summary.
4. The summary fields are the source of truth for performance analysis.
5. You must ONLY use actions from policy.business_actions.
6. Do NOT create new action names.
7. If a suitable action does not exist, choose the closest available action from policy.business_actions.
8. For bid or budget actions, change_pct is REQUIRED and must be a number.
9. For bid or budget actions, change_pct must respect policy.guardrails.
10. If change_pct is not relevant for an action, return null.
11. Do NOT execute live changes.
12. If request.automation_level is recommendation_only, provide recommendations only.
13. Every recommended action must include a clear reason.
14. If data is genuinely insufficient, explain exactly which required field is missing.
15. Keep recommendations practical, conservative, and business-oriented.

Decision guidance:
- Low ROAS and high ACoS indicate inefficient spend.
- High spend with weak conversion suggests reducing bids or budget.
- Good ROAS with low spend may justify careful scaling.
- Low CTR suggests weak relevance, broad targeting, or weak ad/product relevance.
- High CTR but low CVR suggests product page, pricing, reviews, offer, or conversion issue.
- Campaign-level issues may require bid changes, budget changes, campaign pause, or deeper product/keyword analysis.
- Product-level issues may require bid changes, product pause/removal, or product page review if that action is available.
- Keyword-level issues may require bid changes, keyword pause/removal, or negative keyword actions.

Action mapping:
- If you want to reduce budget, use decrease_budget.
- If you want to increase budget, use increase_budget.
- If you want to reduce bid, use decrease_bid.
- If you want to increase bid, use increase_bid.
- If you want to review targeting or search terms, use analyze_keywords if available.
- If you want to review product-level problems, use analyze_products or recommend_product_page_review if available.
- If no change is needed, use keep_current_settings.

Output rules:
- Return only valid JSON.
- Follow the response schema exactly.
- Do not include markdown.
- Do not include explanations outside the JSON.
- Use confidence as a number between 0 and 1.
- Use risk_level as one of: low, medium, high.
- Use priority as one of: low, medium, high.


### Prompt:

Analyze this Amazon Ads decision context and return structured recommendations.

The decision context is provided below as JSON blocks. Treat these blocks as the complete available context.

REQUEST:
{{ JSON.stringify($json.request, null, 2) }}

POLICY:
{{ JSON.stringify($json.policy, null, 2) }}

ENTITY:
{{ JSON.stringify($json.entity, null, 2) }}

SUMMARY:
{{ JSON.stringify($json.summary, null, 2) }}

Your task:
1. Read REQUEST.mode to understand the analysis mode.
2. Read REQUEST.objective to understand what the user wants to optimize.
3. Read POLICY.business_actions and choose actions ONLY from that list.
4. Read POLICY.guardrails and respect all limits.
5. Read ENTITY to understand the object being analyzed.
6. Read SUMMARY to evaluate performance.

Performance interpretation:
- Use SUMMARY.roas, SUMMARY.acos, SUMMARY.ctr, SUMMARY.cvr, SUMMARY.cpc, SUMMARY.sum_spend, SUMMARY.sum_sales, SUMMARY.sum_orders, and SUMMARY.sum_clicks.
- If these fields are present in SUMMARY, do not say that performance data is missing.
- If ROAS is low and ACoS is high, recommend conservative efficiency actions.
- If CTR is low, consider keyword/product relevance issues.
- If CVR is low, consider conversion or product-page issues.

Action rules:
- Use exact action names from POLICY.business_actions.
- Do not invent actions.
- For increase_bid, decrease_bid, increase_budget, or decrease_budget, change_pct must be a number.
- For bid changes, change_pct must be <= POLICY.guardrails.max_bid_change_pct.
- For budget changes, change_pct must be <= POLICY.guardrails.max_budget_change_pct.
- Use conservative changes, usually 5–20%.
- If no safe action is justified, use keep_current_settings.
- If deeper analysis is needed and analyze_products or analyze_keywords is available, you may recommend it.

Automation rules:
- If REQUEST.automation_level is recommendation_only, recommendations are not executed.
- Set requires_human_approval according to POLICY.guardrails.human_approval_required.
- Do not imply that any action has already been applied.

Detail level:
- If REQUEST.detail_level is detailed, include clear reasoning using the provided metrics.
- If REQUEST.detail_level is basic, keep reasoning shorter.

Return only valid JSON according to the response schema.
Return only valid JSON according to the response schema.


### Output:
{
  "decision": {
    "agent_type": "Marketing Optimization Agent for Amazon Ads",
    "diagnosis": "...",
    "recommended_actions": [
      {
        "action": "decrease_bid",
        "target": "CAMP_A",
        "change_pct": 15,
        "priority": "high",
         confidence": 0.9,
        "risk_level": "medium",
        "requires_human_approval": true,
        "reason": "..."
      }
    ],
    "summary_for_user": "..."
  }
}


### 2.2 Execution Agent

Execution Agent is the second AI agent in the system.

It receives the recommendation created by MarketingOptimizationAgent, performs an additional validation step, converts valid recommendations into action records, and writes the result into the n8n database log.

AI model:

GPT-5-mini

### Input:

{
  "request": {...},
  "policy": {...},
  "entity": {...},
  "summary": {...},
  "decision": {...}
}

Main responsibilities:

- read recommended actions from decision
- validate actions against policy.business_actions
- validate bid and budget changes against policy.guardrails
- create action_records for valid recommendations
- create rejected_actions for invalid recommendations
- write one execution log row into the n8n database
- return final execution status

The agent does not perform new marketing analysis.
The agent does not execute live Amazon Ads changes.
The agent only prepares reviewable action records.


### System Message:

You are an Action Execution Agent.

Your only job is to prepare an execution result and insert exactly one row into the agent_action_log table using the Insert Log tool.

You do not perform new marketing analysis.
You do not execute live Amazon Ads changes.
You do not invent new actions.
You only process the previous agent decision.

You receive:
- request
- policy
- entity
- summary
- output

The Insert Log tool writes to exactly one table: agent_action_log.

The agent_action_log table has exactly these columns:
mode, entity_type, entity_id, entity_name, market, automation_level, overall_status, human_review_required, can_execute_live, diagnosis, summary_for_user, execution_summary, action_records_json, full_context_json

When using Insert Log:
- Fill only these columns.
- Do not send any other fields.
- Do not send request as an object.
- Do not send policy as an object.
- Do not send entity as an object.
- Do not send summary as an object.
- Do not send output as an object.
- Do not send execution as an object.
- Do not send action_records as an array.
- action_records_json must be a JSON string.
- full_context_json must be a JSON string.

Validation rules:
- Valid actions must exist in policy.business_actions.
- increase_bid and decrease_bid require numeric change_pct not greater than policy.guardrails.max_bid_change_pct.
- increase_budget and decrease_budget require numeric change_pct not greater than policy.guardrails.max_budget_change_pct.
- Non-bid and non-budget actions may use change_pct = null.
- Invalid actions should be listed in rejected_actions in the final output and inside full_context_json.

Execution rules:
- If request.automation_level is recommendation_only, no live changes are executed.
- If policy.guardrails.do_not_execute_live_changes is true, can_execute_live must be false.
- If policy.guardrails.human_approval_required is true, human_review_required must be true.
- Valid actions should have status pending_human_review.

Use Insert Log exactly once.

After using Insert Log, return only valid JSON in the required response format.
Do not include markdown.
Do not include text outside JSON.


### Prompt:

Create an execution plan and insert one row into the agent_action_log table.

INPUT DATA

REQUEST:
{{ JSON.stringify($json.request, null, 2) }}

POLICY:
{{ JSON.stringify($json.policy, null, 2) }}

ENTITY:
{{ JSON.stringify($json.entity, null, 2) }}

SUMMARY:
{{ JSON.stringify($json.summary, null, 2) }}

DECISION:
{{ JSON.stringify($json.decision, null, 2) }}

TASK

1. Read DECISION.recommended_actions.
2. Validate each action using POLICY.business_actions and POLICY.guardrails.
3. Create action_records for valid actions.
4. Create rejected_actions for invalid actions.
5. Insert exactly one row into agent_action_log using Insert Log.
6. Return the final execution JSON.

ACTION RECORD FORMAT

For each valid action, create this object:

{
  "action": "...",
  "target": "...",
  "target_type": "...",
  "change_pct": 0,
  "priority": "...",
  "risk_level": "...",
  "confidence": 0,
  "status": "pending_human_review",
  "can_execute_live": false,
  "human_review_required": true,
  "reason": "...",
  "execution_note": "Recommendation only. No live change was executed."
}

Use change_pct = null when the action does not require a percentage change.

STATUS LOGIC

Set:
- can_execute_live = false
- human_review_required = POLICY.guardrails.human_approval_required
- execution_mode = REQUEST.automation_level

Set overall_status:
- "pending_human_review" if valid actions > 0 and rejected actions = 0
- "partially_rejected" if valid actions > 0 and rejected actions > 0
- "rejected" if valid actions = 0 and rejected actions > 0
- "logged_only" if there are no actions to process

INSERT LOG INSTRUCTIONS

Use Insert Log exactly once.

Only insert these exact table fields:
mode, entity_type, entity_id, entity_name, market, automation_level, overall_status, human_review_required, can_execute_live, diagnosis, summary_for_user, execution_summary, action_records_json, full_context_json

FINAL RESPONSE

After Insert Log succeeds, return exactly this JSON structure:

{
  "execution": {
    "agent_type": "Action Execution Agent",
    "execution_mode": "...",
    "overall_status": "...",
    "can_execute_live": false,
    "human_review_required": true,
    "actions_total": 0,
    "valid_actions_count": 0,
    "rejected_actions_count": 0,
    "execution_summary": "...",
    "action_records": [],
    "rejected_actions": [],
    "next_step": "human_review",
    "logged_to_action_table": true,
    "summary_for_user": "..."
  }
}


### Output:

{
  "execution": {
    "agent_type": "Action Execution Agent",
    "execution_mode": "recommendation_only",
    "overall_status": "pending_human_review",
    "can_execute_live": false,
    "human_review_required": true,
    "actions_total": 4,
    "valid_actions_count": 4,
    "rejected_actions_count": 0,
    "execution_summary": "Prepared 4 action records for human review. No live changes were executed.",
    "action_records": [
      {
        "action": "decrease_bid",
        "target": "CAMP_A",
        "target_type": "campaign",
        "change_pct": 15,
        "priority": "high",
        "risk_level": "medium",
        "confidence": 0.9,
        "status": "pending_human_review",
        "can_execute_live": false,
        "human_review_required": true,
        "reason": "...",
        "execution_note": "Recommendation only. No live change was executed."
      },
      {
        "action": "analyze_keywords",
        "target": "CAMP_A",
        "target_type": "campaign",
        "change_pct": null,
        "priority": "high",
        "risk_level": "low",
        "confidence": 0.85,
        "status": "pending_human_review",
        "can_execute_live": false,
        "human_review_required": true,
        "reason": "...",
        "execution_note": "Recommendation only. No live change was executed."
      },
      {
        "action": "analyze_products",
        "target": "CAMP_A",
        "target_type": "campaign",
        "change_pct": null,
        "priority": "medium",
        "risk_level": "low",
        "confidence": 0.8,
        "status": "pending_human_review",
        "can_execute_live": false,
        "human_review_required": true,
        "reason": "...",
        "execution_note": "Recommendation only. No live change was executed."
      },
      {
        "action": "decrease_budget",
        "target": "CAMP_A",
        "target_type": "campaign",
        "change_pct": 10,
        "priority": "medium",
        "risk_level": "medium",
        "confidence": 0.75,
        "status": "pending_human_review",
        "can_execute_live": false,
        "human_review_required": true,
        "reason": "...",
        "execution_note": "Recommendation only. No live change was executed."
      }
    ],
    "rejected_actions": [],
    "next_step": "human_review",
    "logged_to_action_table": true,
    "summary_for_user": "..."
  }
}


## 3. Orchestration Layer

### 3.1 Main Orchestrator

Main Orchestrator is the central n8n workflow that runs the full AI Marketing Agent pipeline.

It executes each layer step by step:

1. ContextAssembler
2. MarketingOptimizationAgent
3. Execution Agent
4. Full Log Insert

The user only provides the initial request.
All other context, metrics, policy, decision, and execution objects are created by the system.

### Input:

{
  "request": {
    "mode": "campaign",
    "conditions": {
      "campaign_id": "CAMP_A",
      "date_from": "2026-04-20"
    },
    "objective": {
      "primary": "increase_efficiency",
      "secondary": [
        "reduce_acos",
        "improve_roas"
      ]
    },
    "additions": "",
    "detail_level": "detailed",
    "automation_level": "recommendation_only"
  }
}

Processing flow:

1. ContextAssembler builds the full decision context:

{
  "request": {...},
  "policy": {...},
  "entity": {...},
  "summary": {...}
}

2. MarketingOptimizationAgent analyzes the context and returns:

{
  "decision": {...}
}

3. Execution Agent validates the decision and returns:

{
  "execution": {...}
}

4. Main Orchestrator merges all outputs and writes the full result into the final log table.

### Final Output:

{
  "request": {...},
  "policy": {...},
  "entity": {...},
  "summary": {...},
  "decision": {...},
  "execution": {...}
}
