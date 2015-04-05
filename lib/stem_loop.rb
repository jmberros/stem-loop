class StemLoop
  def stockhlm_cmodel_job(accession_code)
    stockhom_msa     = Rfam.new.download_stockholm accession_code
    covariance_model = Infernal.new.cmbuild stockhom_msa
    job_script       = CalibrationScript.new.write_script covariance_model, true
  end
end
