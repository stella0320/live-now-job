
import script.job.indievox_job as indievox_job
import script.job.tixcraft_job as tixcraft_job

if __name__ == '__main__':
    print('----Indievox Job Start-----')
    run_indievox_job = indievox_job.IndievoxJob()
    run_indievox_job.run()
    print('----Indievox Job End-----')

    print('----Tixcraft Job Start-----')
    # run_tixcraft_job = tixcraft_job.TixcraftJob()
    # run_tixcraft_job.run()
    print('----Tixcraft Job End-----')
