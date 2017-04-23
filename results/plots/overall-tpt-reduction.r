library(tikzDevice)
library(ggplot2)
library(scales)
#For some reason, Rstudio needs to know the time zone...
options(tz = "CA")

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) {
    stop("Missing arguments")
}

input_csv <- NULL
output_directory <- NULL

if (length(args) == 1) {
    input_csv <- args[1]
    output_directory <- "."
} else {
    input_csv <- args[1]
    output_directory <- args[2]
}

output_file <- file.path(output_directory, "overall-tpt-reduction.tex")

tikz(file = output_file, width = 3.3, height = 2.2)
iops_data <- read.csv(input_csv)
iops_data$logs <- with(iops_data, leaders + followers)

plot <- ggplot(iops_data, aes(x = logs, y = iops, colour = type, shape = type)) +
    geom_point() +
    geom_smooth(method = "auto") +
    scale_y_continuous(name = "Throughput (IOPS)") +
    scale_x_continuous(name = "Number of Files") +
    theme(legend.position = c(0.85, 0.8), axis.line = element_line(colour = "black"), panel.grid.major = element_blank(), panel.grid.minor = element_blank(), panel.border = element_blank(), panel.background = element_blank()) +
    expand_limits(x = 1, y = 400) +
    guides(colour = guide_legend("Storage Type"), shape = guide_legend("Storage Type"))

# legend.position="top", legend.box = "horizontal",
#This line is only necessary if you want to preview the plot right after compiling
print(plot)

#Necessary to close or the tikxDevice .tex file will not be written
dev.off()