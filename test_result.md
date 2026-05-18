#====================================================================================================
# START - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================

# THIS SECTION CONTAINS CRITICAL TESTING INSTRUCTIONS FOR BOTH AGENTS
# BOTH MAIN_AGENT AND TESTING_AGENT MUST PRESERVE THIS ENTIRE BLOCK

# Communication Protocol:
# If the `testing_agent` is available, main agent should delegate all testing tasks to it.
#
# You have access to a file called `test_result.md`. This file contains the complete testing state
# and history, and is the primary means of communication between main and the testing agent.
#
# Main and testing agents must follow this exact format to maintain testing data. 
# The testing data must be entered in yaml format Below is the data structure:
# 
## user_problem_statement: {problem_statement}
## backend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.py"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## frontend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.js"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## metadata:
##   created_by: "main_agent"
##   version: "1.0"
##   test_sequence: 0
##   run_ui: false
##
## test_plan:
##   current_focus:
##     - "Task name 1"
##     - "Task name 2"
##   stuck_tasks:
##     - "Task name with persistent issues"
##   test_all: false
##   test_priority: "high_first"  # or "sequential" or "stuck_first"
##
## agent_communication:
##     -agent: "main"  # or "testing" or "user"
##     -message: "Communication message between agents"

# Protocol Guidelines for Main agent
#
# 1. Update Test Result File Before Testing:
#    - Main agent must always update the `test_result.md` file before calling the testing agent
#    - Add implementation details to the status_history
#    - Set `needs_retesting` to true for tasks that need testing
#    - Update the `test_plan` section to guide testing priorities
#    - Add a message to `agent_communication` explaining what you've done
#
# 2. Incorporate User Feedback:
#    - When a user provides feedback that something is or isn't working, add this information to the relevant task's status_history
#    - Update the working status based on user feedback
#    - If a user reports an issue with a task that was marked as working, increment the stuck_count
#    - Whenever user reports issue in the app, if we have testing agent and task_result.md file so find the appropriate task for that and append in status_history of that task to contain the user concern and problem as well 
#
# 3. Track Stuck Tasks:
#    - Monitor which tasks have high stuck_count values or where you are fixing same issue again and again, analyze that when you read task_result.md
#    - For persistent issues, use websearch tool to find solutions
#    - Pay special attention to tasks in the stuck_tasks list
#    - When you fix an issue with a stuck task, don't reset the stuck_count until the testing agent confirms it's working
#
# 4. Provide Context to Testing Agent:
#    - When calling the testing agent, provide clear instructions about:
#      - Which tasks need testing (reference the test_plan)
#      - Any authentication details or configuration needed
#      - Specific test scenarios to focus on
#      - Any known issues or edge cases to verify
#
# 5. Call the testing agent with specific instructions referring to test_result.md
#
# IMPORTANT: Main agent must ALWAYS update test_result.md BEFORE calling the testing agent, as it relies on this file to understand what to test next.

#====================================================================================================
# END - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================



#====================================================================================================
# Testing Data - Main Agent and testing sub agent both should log testing data below this section
#====================================================================================================

user_problem_statement: "Pull all text data for the Sea World San Antonio: Explorer's Reef app strictly from the provided PDF spreadsheet; do not populate from the internet. Preserve user-uploaded image overrides. Empty PDF cells should remain blank."

backend:
  - task: "Verbatim PDF data extraction"
    implemented: true
    working: true
    file: "/app/backend/parse_verbatim.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "main"
        comment: "Rebuilt the entire PDF parsing pipeline using pdfplumber char-level positions. Algorithm: read chars in document order, detect cell boundaries via x-resets and forward gaps (>8pt), then snap each cell's starting x to known column ranges. Added post-processors to split run-together natural/nifty cells (region-word terminator detection) and can_eat/description merges (trailing color list + 'Technically'/'NO!' prefix peeling). Resulting fish_dataset.json now has 417 verbatim entries with diet/longevity/conservation/poison/swsa/natural/nifty/can_eat/description/scientific fields straight from the PDF. Scientific names re-exported to scientific_names.json (415 entries)."
      - working: true
        agent: "testing"
        comment: "Verified verbatim PDF data via 34 backend assertions in /app/backend_test.py against the deployed URL https://fish-search-app.preview.emergentagent.com/api. fish_count=417 (>=410 required). Achilles tang record matches PDF VERBATIM: name='achilles tang', scientific_name='Acanthurus achilles', diet='Omnivore', longevity='15 years', conservation_status='LC', poison_toxin='no', nifty_facts contains 'scalpel', colors include black/blue/orange. swsa filter for 'turtle reef' returns 121 fish all containing 'turtle reef' in swsa_habitats. All 34/34 assertions PASSED."
  - task: "Backend serves verbatim PDF data"
    implemented: true
    working: true
    file: "/app/backend/fish_data.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "main"
        comment: "Removed all text normalization (no more lowercasing diet, no 'Unknown' fallbacks). Empty PDF fields stay as empty strings per user choice (option c). User-uploaded image overrides (clown fish, agitated carpet anemone, bicolor fox face, bignose unicorn tang, black boring sea urchin, black brittlestar) are preserved. Scientific names load from scientific_names.json (PDF-sourced)."
      - working: true
        agent: "testing"
        comment: "All 6 review-requested API scenarios verified PASS via /app/backend_test.py: (1) GET /api/ returns fish_count=417 >=410. (2) GET /api/fishes?q=achilles returns exactly 1 fish with all required fields matching exactly. (3) GET /api/fishes?q=clown returns 11 fishes including 'clown fish' whose image_url contains 'customer-assets' (user override preserved). (4) GET /api/filters returns all required keys; diets contain Omnivore/Carnivore/Herbivore, conservation contains 'LC', can_eat contains 'Technically' and 'NO!'. (5) GET /api/fishes?swsa_habitats=turtle+reef returns 121 fish all containing 'turtle reef'. (6) GET /api/fishes/1 returns achilles tang with all standard fields populated. No failing assertions."

frontend:
  - task: "Web UI rendering verbatim PDF fields"
    implemented: true
    working: "NA"
    file: "/app/frontend/app/index.tsx, /app/frontend/app/fish/[id].tsx"
    stuck_count: 0
    priority: "medium"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "No frontend changes in this iteration; verified visually via screenshot that the new dataset renders cleanly (Achilles Tang shows scientific name + Omnivore + 15 years + LC + Technically + Indo-Pacific reefs all verbatim from the PDF). 417 species displayed instead of previous 342."

metadata:
  created_by: "main_agent"
  version: "2.0"
  test_sequence: 4
  run_ui: false

test_plan:
  current_focus:
    - "Verbatim PDF data extraction"
    - "Backend serves verbatim PDF data"
  stuck_tasks: []
  test_all: false
  test_priority: "high_first"

agent_communication:
  - agent: "testing"
    message: "Ran comprehensive backend test suite against deployed URL https://fish-search-app.preview.emergentagent.com/api via /app/backend_test.py — 34/34 assertions passed. (1) /api/ returns fish_count=417. (2) /api/fishes?q=achilles returns exactly 1 record; every PDF-verbatim field matches expectations (name='achilles tang', diet='Omnivore', longevity='15 years', conservation_status='LC', poison_toxin='no', scientific_name='Acanthurus achilles', nifty_facts contains 'scalpel', colors include black/blue/orange). (3) /api/fishes?q=clown returns 11 fishes including 'clown fish' with image_url containing 'customer-assets' (user override preserved). (4) /api/filters returns all required keys non-empty; diets contain Omnivore/Carnivore/Herbivore, conservation contains 'LC', can_eat contains 'Technically' and 'NO!'. (5) /api/fishes?swsa_habitats=turtle+reef returns 121 fish all containing 'turtle reef'. (6) /api/fishes/1 returns the full achilles tang record. No failures detected — main agent can summarise and finish."
  - agent: "main"
    message: "Completely rebuilt the PDF -> JSON pipeline. The new parser (parse_verbatim.py) extracts text using pdfplumber character positions + document-order traversal with x-reset/forward-gap detection, plus targeted post-processors for the few rows where adjacent cells touch without a gap. fish_dataset.json now has 417 fish with all text VERBATIM from the source PDF; no internet/LLM/Wikipedia text. User-uploaded image overrides for clown fish, brittlestar, anemone, fox face, unicorn tang, and sea urchin are preserved. Please backend-test: 1) GET /api/ returns fish_count >= 410 2) GET /api/fishes?q=achilles returns Achilles Tang with diet=Omnivore, longevity='15 years', conservation_status=LC, nifty_facts contains 'scalpel' 3) GET /api/fishes?q=clown returns multiple clown-* species, with 'clown fish' having the custom image_url containing 'customer-assets' 4) GET /api/filters returns lists for colors, diets, swsa_habitats, conservation, can_eat 5) Filtering by swsa_habitat='turtle reef' returns >0 fish."
