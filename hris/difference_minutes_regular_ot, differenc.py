difference_minutes_regular_ot, difference_hours_regular_ot, difference_minutes_regular_sc, difference_hours_regular_sc, difference_minutes_regular_hn, difference_hours_regular_hn, difference_hours_regular, difference_minutes_regular = compute_time_difference(time_in, time_out,
                            break_in, break_out,
                            official_office_in,
                            official_office_out,
                            official_honorarium_time_in,
                            official_honorarium_time_out,
                            official_servicecredit_time_in,
                            official_servicecredit_time_out,
                            official_overtime_time_in,
                            official_overtime_time_out,
                            employment_status)





                             
    # class OfficialTIme(models.Model):
    #     CATEGORY = (
    #             ('Regular', 'Regul2ar'),
    #             ('Job Order','Job Order'),
    #             ('Job Order','Job Order'),
    #             )
    #     name = models.CharField(max_length = 200, null= True)
    #     price = models.FloatField(null=True)
    #     category = models.CharField(max_length = 200, null= True, choices = CATEGORY)
    #     description = models.CharField(max_length = 200, null= True, blank = True)
    #     date_created = models.DateTimeField(auto_now_add=True, null= True)
    
    # def __str__(self):
    #     return self.name
    
    
    # class Order(models.Model):
    #     STATUS = (
    #             ('Pending', 'Pending'),
    #             ('Out for Delivery','Out for Delivery'),
    #             ('Delivered', 'Delivered'),
    #             )

    #     customer = models.ForeignKey(Employee, null=True, on_delete= models.SET_NULL)
    #     product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    #     date_created = models.DateTimeField(auto_now_add=True, null= True)
    #     status = models.CharField(max_length = 200, null=True, choices=STATUS)
    #     note = models.CharField(max_length = 1000, null=True)
        
    #     def __str__(self):
    #         return self.product.name

