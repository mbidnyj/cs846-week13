ENGINEERING REQUIREMENTS
1 - design a structured context prompt
2 - LLM output is a draft that have to be reviewed

CODE COMPREHENSION
1 - provide project specific examples and context (not relevant any more: coding agents are trained to do it better)
2 - focus on higher-level functionality when designing prompts, not the implementation

CODE EXECUTION
1 - specify context about the project, like how to run tools
2 - work in short, iterative cycles (valid, context window get messy)

DEBUGGING
1 - control prompt details based on solution certainty
2 - specify edge cases and all important details - if you'll not, LLM will decide it themselves

CODE REVIEW
1 - understand your intent before creating a prompt
2 - create an instruction file (like claudemd)

PERFORMANCE
1 - ask LLM to analyze complexity before implementation
2 - check for dead code before optimizing

LOGGING
1 - select one looging library and stick with it for the whole project
2 - specify exactly what should be logged, because if not - LLM would create too many of them