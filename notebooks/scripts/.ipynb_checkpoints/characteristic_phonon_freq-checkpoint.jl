using PolaronMobility
using DelimitedFiles

root = "../../raw_data/hybrid_calcs_raw/"
dirs = readdir(root);

phonon_freqs = []
for d in dirs
    if endswith(d, "dfpt")
        IR_data_file = string(root, d , "/IR-PeakTable.dat")
        IR_data = readdlm(IR_data_file, skipstart=1)
        phonon_freq = HellwarthBScheme(IR_data);
        push!(phonon_freqs, [d, phonon_freq]);
    end
end

freq_array = hcat(phonon_freqs...)
freq_array = permutedims(freq_array)

writedlm("../../processed_data/characteristic_frequencies.csv", freq_array, ",")
