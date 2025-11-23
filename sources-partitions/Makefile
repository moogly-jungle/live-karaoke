odt = $(wildcard *.odt)
odc = $(wildcard *.odc)
dest_dir = ../docs/partitions

files = $(patsubst %.odt,${dest_dir}/%.png,${odt})
files += $(patsubst %.odc,${dest_dir}/%.png,${odc})

all: ${files}

${dest_dir}/%.png: %.odt
	libreoffice --view --convert-to png --outdir ${dest_dir} $<

${dest_dir}/%.png: %.odc
	libreoffice --view --convert-to png --outdir ${dest_dir} $<
