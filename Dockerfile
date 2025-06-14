FROM continuumio/miniconda3

# Use bash as the default shell
SHELL ["/bin/bash", "--login", "-c"]

WORKDIR /app

# Copy environment.yml first for better caching
COPY environment.yml .

# Create the conda environment
RUN conda env create -f environment.yml

# Copy the rest of the code
COPY . .

# Copy and set entrypoint
COPY entrypoint.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python", "flagellar_motors_detection/dataset.py"]
