sources = $(wildcard *.odt)
dest_dir = ../docs/partitions

files = $(patsubst %.odt,${dest_dir}/%.png,${sources})

all: ${files}

${dest_dir}/%.png: %.odt
	libreoffice --view --convert-to png --outdir ${dest_dir} $<
