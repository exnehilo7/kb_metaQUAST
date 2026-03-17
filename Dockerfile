FROM kbase/sdkpython:3.8.0
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

RUN apt-get update \
    # && apt-get upgrade -y \
    && apt-get install -y \
        zlib1g-dev \
        wget \
    && rm -rf /var/lib/apt/lists/* 
#     && conda install -yc bioconda quast

# RUN conda config --add channels bioconda \
#     && conda create -y -n conda_quast \
#         quast \
#     && conda clean -a -y

# ENV PATH=/opt/conda3/envs/conda_quast/bin:$PATH

# RUN conda install -yc bioconda quast

RUN cd /usr/local/bin \
    && wget https://github.com/ablab/quast/releases/download/quast_5.3.0/quast-5.3.0.tar.gz \
    && tar -xzf quast-5.3.0.tar.gz \
    && cd quast-5.3.0 \
    && ./setup.py install \
    && rm -rf /usr/local/bin/quast-5.3.0.tar.gz



# RUN cd /usr/local/bin \
#     && git clone https://github.com/ablab/quast.git 
#     && /usr/local/bin/quast/quast.py 


# QUAST output:
# Text versions of total report are saved to /kb/module/quast-5.3.0/quast_results/results_2026_03_16_20_47_55/report.txt, report.tsv, and report.tex
# Text versions of transposed total report are saved to /kb/module/quast-5.3.0/quast_results/results_2026_03_16_20_47_55/transposed_report.txt, transposed_report.tsv, and transposed_report.tex
# HTML version (interactive tables and plots) is saved to /kb/module/quast-5.3.0/quast_results/results_2026_03_16_20_47_55/report.html
# Icarus (contig browser) is saved to /kb/module/quast-5.3.0/quast_results/results_2026_03_16_20_47_55/icarus.html
# Log is saved to /kb/module/quast-5.3.0/quast_results/results_2026_03_16_20_47_55/quast.log

# MetaQUAST output:
# Output for combined reference genome is located inside combined_reference subdirectory of the output directory provided with -o (or in quast_results/latest). An output for each reference genome is placed into separate directory inside <quast_output_dir>/runs_per_reference directory. Also, plots and reports for key metrics are saved under <quast_output_dir>/summary/. Combined HTML report is saved to <quast_output_dir>/report.html.
# --Metric-level plots--
# These plots are created for each key metric to show its values for all assemblies vs all reference genomes. References on the plot are sorted by the mean value of this metric in all assemblies. References are always sorted from the best results to the worst ones, thus the plot can be descending or ascending depend on the metric.
# --Metric-level reports (TXT, TSV and TEX versions)--
# These files contain the same information as the metric-level plots, but in different formats: simple text format, tab-separated format, and LaTeX.
# --Summary HTML-report--
# Summary HTML-report is created on the basis of HTML-report in combined_quast_output/. Each row is expandable and contains data for all reference genomes. You can view results separately for each reference genome by clicking on a row preceded by plus sign
# --Krona charts--
# Krona pie charts show assemblies and dataset taxonomic profiles. Relative species abundance is calculated based on the total aligned length of contigs aligned to corresponding reference genome. Charts are created for each assembly and one additional chart is created for all assemblies altogether.
# Note: these plots are created only in de novo evaluation mode (MetaQUAST without reference genomes).
# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
