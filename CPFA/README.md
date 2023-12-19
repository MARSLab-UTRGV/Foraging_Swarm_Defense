# Swarm Robotics Simulation

This repository hosts the code for running swarm robotics simulations in ARGoS, focusing on robot behavior under misleading trail attacks. The simulations are configured through Python scripts and executed within the ARGoS environment.

## Getting Started

### Prerequisites
- ARGoS simulation environment installed on your system.
- Python 3.x for running configuration and analysis scripts.

### Configuration
Explore `xml_config.py` for functions to create or update ARGoS configuration files. This script is essential for setting up various parameters for your simulation. Each function and parameter is well-documented with comments in the file.

### Running Simulations

#### Quick Test
Run a quick test simulation with a visual display using the `quickTest` function in `run.py`:
```python
def quickTest():
    # [Configuration code here...]
    os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")
```

#### Ensure Function Execution in Main Block
When running `run.py`, make sure that the `quickTest()` function is called within the `if __name__ == "__main__":` block. This block is a standard Python idiom for conditionally executing code when the script is run as the main program rather than being imported as a module. 

Here's how to ensure `quickTest()` is properly called:

```python
if __name__ == "__main__":
    # Uncomment the following line to run quickTest when this script is executed
    quickTest()
```

By placing your function call inside this block, you ensure that `quickTest()` executes when `run.py` is run directly. If you're running different experiments, you can comment or uncomment the relevant function calls in this block as needed.

#### Example Main Block in run.py
The `if __name__ == "__main__":` block in `run.py` might look like this:

```python
if __name__ == "__main__":
    # Other experiment function calls (commented out)
    # Experiment1(30), Experiment2(30), etc.

    # Uncomment the line below to run the quickTest function
    quickTest()
```

Ensure that other experiment function calls are commented out when you want to run `quickTest`, to avoid unintentional execution of multiple experiments simultaneously.

### Configuration with `xml_config.py`

The `xml_config.py` script is crucial for setting up your simulation parameters. It defines a class that handles the creation and updating of ARGoS configuration files.

#### Using `xml_config.py` in Your Scripts

- **Class Definition**: `xml_config.py` defines a class that encapsulates the configuration settings for your simulation. Familiarize yourself with the class methods and attributes to effectively use it in your experiments.

- **Instantiating the Class**: In your `run.py` or any custom scripts, you must instantiate this class to access its functionalities. 

    ```python
    import xml_config

    def yourExperimentFunction():
        # Create an instance of the configuration class
        config_instance = xml_config.C_XML_CONFIG(your_parameters)
        
        # Utilize various methods of the class to set up your simulation
        config_instance.setBotCount(24)
        config_instance.setDetractorPercentage(25, True)
        # ... other configuration methods ...

        # Finally, create the XML configuration file
        config_instance.createXML()
    ```

- **Custom Scripts**: When writing custom scripts, ensure that you import `xml_config`, create an instance of its class, and use its methods to configure your simulation before running it.

- **Modularity and Reusability**: The class in `xml_config.py` is designed to be modular and reusable across different experimental setups. Leverage this to maintain consistency and efficiency in your simulation configurations.

Remember to always create an instance of the class defined in `xml_config.py` in your experiment scripts. This instance will be your primary interface for configuring and generating the necessary XML files for running simulations in ARGoS.

### Important Functions
- `setBotCount(botCount)`: Sets the total number of foraging robots in the simulation.
  - Example usage: `XML.setBotCount(24)`
  - There is an issue currently with how this is done. As a workaround, also set `XML.BOT_COUNT` to the desired number of normal foragers otherwise it will default to 32.
- `setDetractorPercentage(percent, static_foragers)`: Configures the percentage of detractors in the robot swarm.
  - `static_foragers = True` keeps the number of foragers constant while adding detractors.
  - `static_foragers = False` will keep the total number of robots constant while removing the desired percentage of foragers and replacing them with detractors.
  - Example usage: `XML.setDetractorPercentage(25, True)`

#### Plotting Results
To plot experiment results, use the separate plotting script provided or use the some of the plotting functions in `run.py` as templates.

## Running a Simulation
To run a simulation, execute the desired function in `run.py` or your custom script:
```bash
python run.py
```