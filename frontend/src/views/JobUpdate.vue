<template>
    <form method="POST">
        <div class="row">
            <div class="col-md">
                <div class="p-3 py-5">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="text-right">Vacancy</h4>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-6"><label class="labels">Title</label>
<input type="text" name="title" class="form-control" required="true"/>
                        </div>
                        <div class="col-md-6"><label class="labels">Description</label>
<input type="text" name="description" class="form-control" required="true"/>
                        </div>
                    </div>
                    <div class="row ">

                        <div class="col-md-12 mt-2"><label class="labels">Salary from</label>
<input type="number" name="salary_from" class="form-control" required="true"/>
                        </div>
                        <div class="col-md-12 mt-2"><label class="labels">Salary up to</label>
<input type="number" name="salary_to" class="form-control" required="true"/>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-warning mt-4">Update</button>
                </div>
            </div>
        </div>
    </form>

</template>

<script>

</script>