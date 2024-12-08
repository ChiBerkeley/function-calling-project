
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)



![Logo](https://www.ischool.berkeley.edu/sites/default/files/styles/fullscreen/public/2024-11/image_1.png?itok=8VS8MJyH)


# SynthCall

Synthcall is a project created by students from MIDS program at UC Berkeley. This project aims at provding a feasible, low cost solution that enables function calling/tool-use by introducing a data generation pipeline. This MVP contains example functions, generation pipeline, evalutions  and a front end design. 


## Authors

- [@rennsport](https://github.com/rennsport)
- [@ChiBerkeley](https://www.github.com/ChiBerkeley)
- [@edwardkshin](https://www.github.com/edwardkshin)
- [@mthottam](https://www.github.com/mthottam)


## Folders

- `/function_sets`
    - Contains example functions with deatiled descriptions for data generation and function calling

- `/instruct`
    - Contains data generation pipeline and many example of function calling dataset based on given function descriptions

- `/eval`
    - Includes a list of notebooks that demostrate the evaluation process. There are examples combine Ragas, AWS bedrock, Langchain to measure the relevancy of generated data. 

- `/front_end`
    - An front-end example that uses language chain and gradio to demostrate data generation and function calling. These files consolidate the work from `/instruct` which includes prompt engineering and structured output



## Related

SynthCall MIDS Website

[SynthCall](https://www.ischool.berkeley.edu/projects/2024/synthcall)


## License

[MIT](https://choosealicense.com/licenses/mit/)

