/**
 * PSYCH_DATABASE Schema Definitions
 * JSDoc type definitions for all entry types in the psychiatric encyclopedia.
 * This file is NOT loaded at runtime — it exists for editor IntelliSense and developer reference.
 */

// ═══════════════════════════════════════════════════════════════
// Common Types
// ═══════════════════════════════════════════════════════════════

/**
 * @typedef {"matrix" | "text" | "table" | "flowchart" | "calculator" | "checklist"} EntryType
 */

/**
 * @typedef {Object} BaseEntry
 * @property {string} id - Unique identifier (e.g., "alg_agitation")
 * @property {string} cmd_alias - CLI command alias (e.g., "agitation")
 * @property {EntryType} type - Determines which renderer and data fields are used
 * @property {string} category - Display category (e.g., "Ургентная психиатрия")
 * @property {string} title - Display title
 * @property {string[]} tags - Search keywords
 * @property {string[]} related - IDs of related entries (validated at build time)
 * @property {string} description - Short summary (used in cards/search results)
 * @property {string} lastUpdated - ISO date "YYYY-MM-DD" of last content update
 * @property {string[]} sources - Citations / references for the clinical content
 */

// ═══════════════════════════════════════════════════════════════
// Matrix Type
// ═══════════════════════════════════════════════════════════════

/**
 * @typedef {Object} MatrixPhase
 * @property {string} title - Phase title
 * @property {string} desc - Phase description
 */

/**
 * @typedef {Object} MatrixCurrent
 * @property {string} title - Current state title
 * @property {string} pheno - Phenomenological description
 * @property {string} neuro - Neurobiological mechanism
 * @property {string} tactic - Treatment tactics
 */

/**
 * @typedef {Object} MatrixData
 * @property {MatrixPhase[]} past - Past / risk factors / preceding phases
 * @property {MatrixCurrent} current - Current state: phenotype, neurobiology, treatment
 * @property {MatrixPhase[]} future - Outcomes / prognosis / complications
 */

/**
 * @typedef {BaseEntry & { type: "matrix", matrix: MatrixData }} MatrixEntry
 */

// ═══════════════════════════════════════════════════════════════
// Text Type
// ═══════════════════════════════════════════════════════════════

/**
 * @typedef {BaseEntry & { type: "text", content: string }} TextEntry
 */

// ═══════════════════════════════════════════════════════════════
// Table Type
// ═══════════════════════════════════════════════════════════════

/**
 * @typedef {BaseEntry & { type: "table", tableHeaders: string[], tableRows: string[][] }} TableEntry
 */

// ═══════════════════════════════════════════════════════════════
// Flowchart Type
// ═══════════════════════════════════════════════════════════════

/**
 * @typedef {Object} FlowchartOption
 * @property {string} label - Option text shown to user
 * @property {string} next - ID of the next step
 */

/**
 * @typedef {Object} FlowchartStep
 * @property {string} [question] - Question text (for decision nodes)
 * @property {string} [info] - Additional info shown with the question
 * @property {FlowchartOption[]} [options] - Available choices
 * @property {boolean} [result] - If true, this is a terminal/result node
 * @property {string} [title] - Title for result nodes
 * @property {string} [content] - Content for result nodes
 */

/**
 * @typedef {Object} FlowchartData
 * @property {string} start - ID of the first step
 * @property {Object.<string, FlowchartStep>} steps - Map of step ID to step data
 */

/**
 * @typedef {BaseEntry & { type: "flowchart", flowchart: FlowchartData }} FlowchartEntry
 */

// ═══════════════════════════════════════════════════════════════
// Calculator Type
// ═══════════════════════════════════════════════════════════════

/**
 * @typedef {Object} ScaleItem
 * @property {string} id - Item identifier
 * @property {string} text - Question / item text
 * @property {number} max - Maximum score for this item
 */

/**
 * @typedef {Object} ScoringRange
 * @property {[number, number]} range - [min, max] inclusive
 * @property {string} label - Severity label
 * @property {string} color - HEX color for display
 * @property {string} action - Recommended action text
 */

/**
 * @typedef {Object} EquivalenceItem
 * @property {string} drug - Drug name
 * @property {number} dose_eq - Equivalent dose
 * @property {string} unit - Unit of measurement
 */

/**
 * @typedef {Object} CalculatorData
 * @property {"scale" | "equivalence"} calcType - Calculator mode
 * @property {string} [reference] - Reference drug/dose (for equivalence type)
 * @property {ScaleItem[] | EquivalenceItem[]} items - Scale questions or equivalence items
 * @property {ScoringRange[]} [scoring] - Score interpretation ranges (for scale type)
 * @property {string | string[]} [labels] - Response option labels
 */

/**
 * @typedef {BaseEntry & { type: "calculator", calculator: CalculatorData }} CalculatorEntry
 */

// ═══════════════════════════════════════════════════════════════
// Checklist Type
// ═══════════════════════════════════════════════════════════════

/**
 * @typedef {Object} ChecklistItem
 * @property {string} id - Item identifier
 * @property {string} text - Checklist item text
 */

/**
 * @typedef {Object} ChecklistSection
 * @property {string} title - Section title
 * @property {ChecklistItem[]} items - Items in this section
 */

/**
 * @typedef {Object} ChecklistData
 * @property {ChecklistSection[]} sections - Grouped checklist sections
 */

/**
 * @typedef {BaseEntry & { type: "checklist", checklist: ChecklistData }} ChecklistEntry
 */

// ═══════════════════════════════════════════════════════════════
// Union Type
// ═══════════════════════════════════════════════════════════════

/**
 * @typedef {MatrixEntry | TextEntry | TableEntry | FlowchartEntry | CalculatorEntry | ChecklistEntry} PsychEntry
 */

module.exports = {};
